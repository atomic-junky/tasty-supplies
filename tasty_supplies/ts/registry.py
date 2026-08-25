"""Collects what the catalog declares, checks it, and names the recipes.

Every plugin of the pipeline reaches the same instance through
``ctx.inject(Registry)``.
"""

import importlib
import logging
from typing import Any, Dict, List, Optional, Tuple

from .declaration import REGISTERED
from .item import Item
from .recipe import Cooked, Recipe, RecipeSpec, ref_key

logger = logging.getLogger(__name__)

#: Supports known to be wrong, tolerated until the fix lands with its own
#: in-game test, since it changes what the recipes accept: ``ice_cream_cone``
#: sits on ``bread``, and ``cheese_slice`` shares its support with
#: ``fried_egg``.
KNOWN_SUPPORT_ISSUES = frozenset({"ice_cream_cone", "cheese_slice", "fried_egg"})


class Registry:
    """Every item and recipe of the pack, ready to be emitted."""

    def __init__(self, ctx: Any = None) -> None:
        self.ctx = ctx
        self.items: Dict[str, Item] = {}
        self.recipes: List[RecipeSpec] = []
        self.categories: List[str] = []
        self._by_class: Dict[type, Item] = {}
        self._recipe_ids: Dict[str, int] = {}

    def load(self, package: str = "ts.catalog") -> None:
        """Import the catalog and turn every declared class into pack data."""

        catalog = importlib.import_module(package)

        labels: Dict[str, str] = {}
        for name in catalog.CATEGORIES:
            module = importlib.import_module(f"{package}.{name}")
            labels[name] = getattr(module, "CATEGORY", name)
        self.categories = list(labels.values())

        prefix = f"{package}."

        def category_of(cls: type) -> str:
            # Where the class lives, not when it was imported: a module may
            # pull in items from another category.
            path = cls.__module__.removeprefix(prefix)
            return labels.get(path.split(".")[0], "misc")

        declared: List[Tuple[type, str]] = [
            (cls, category_of(cls)) for cls in REGISTERED
        ]

        for cls, category in declared:
            if issubclass(cls, Item):
                self._add_item(cls, category)

        for cls, category in declared:
            if issubclass(cls, Item):
                owner = self._by_class[cls]
                self._add_recipes(owner.recipes(), owner, owner.id, category, cls.book)
            elif issubclass(cls, Recipe):
                holder = cls()
                self._add_recipes(
                    holder.recipes(), cls.result, cls.id, category, cls.book
                )

        self.check()

    def _add_item(self, cls: type, category: str) -> None:
        if cls.id in self.items:
            raise ValueError(
                f"Two items share the id {cls.id!r}: {type(self.items[cls.id]).__name__}"
                f" and {cls.__name__}."
            )
        self._store(cls())

    def _store(self, item: Item) -> None:
        self.items[item.id] = item
        self._by_class[type(item)] = item

    def _add_recipes(
        self,
        specs: List[RecipeSpec],
        result: Any,
        base_id: str,
        category: str,
        book: bool = True,
    ) -> None:
        for spec in specs:
            if spec.result is None:
                spec.result = result
            spec.ts_category = category
            spec.book = spec.book and book
            spec.resolve(self.resolve)

            recipe_id = spec.id or self._next_recipe_id(base_id)
            if isinstance(spec, Cooked):
                for variant in spec.expand():
                    variant.id = f"{recipe_id}_{variant.suffix}"
                    self.recipes.append(variant)
            else:
                spec.id = recipe_id
                self.recipes.append(spec)

    def _next_recipe_id(self, base_id: str) -> str:
        """``apple_pie``, then ``apple_pie_1`` for the next recipe of that item."""

        if base_id not in self._recipe_ids:
            self._recipe_ids[base_id] = 0
            return base_id
        self._recipe_ids[base_id] += 1
        return f"{base_id}_{self._recipe_ids[base_id]}"

    def resolve(self, ref: Any) -> Any:
        """Turn an item class into its instance, leave anything else alone."""

        if isinstance(ref, type) and issubclass(ref, Item):
            item = self._by_class.get(ref)
            if item is None:
                raise ValueError(
                    f"{ref.__name__} is referenced but not declared in the catalog."
                )
            return item
        return ref

    def get(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)

    def check(self) -> None:
        """Catch what used to fail silently."""

        # Only the recipes vanilla resolves; ours read the model data.
        ingredients = {
            ref_key(ingredient)
            for recipe in self.recipes
            if recipe.matches_support
            for ingredient in recipe.ingredients()
            if isinstance(ingredient, Item)
        }

        by_support: Dict[str, List[str]] = {}
        for item in self.items.values():
            by_support.setdefault(item.support.id, []).append(item.id)

        for item_id in sorted(ingredients - KNOWN_SUPPORT_ISSUES):
            item = self.items[item_id]
            sharing = [
                other for other in by_support[item.support.id] if other != item_id
            ]

            if not item.support.dedicated:
                raise ValueError(
                    f"{item_id!r} is used as an ingredient but sits on the generic"
                    f" support {item.support.id!r}: any vanilla one would do. Give it"
                    f" a dedicated support in bases.py."
                )
            if sharing:
                raise ValueError(
                    f"{item_id!r} is used as an ingredient but shares the support"
                    f" {item.support.id!r} with {', '.join(sorted(sharing))}: recipes"
                    f" cannot tell them apart."
                )

        seen: Dict[tuple, str] = {}
        for recipe in self.recipes:
            key = recipe.duplicate_key()
            if key in seen:
                logger.warning("Recipes %s and %s are identical.", seen[key], recipe.id)
            else:
                seen[key] = recipe.id
