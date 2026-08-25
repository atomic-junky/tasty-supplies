"""The in-game recipe book.

Every recipe gets a page, unless it opts out with ``book = False``. The book
itself is a catalog item; only its pages are filled in here.
"""

import logging
from typing import Dict, List

from beet import Context, Font

from ..recipe import RecipeSpec, ref_key
from ..registry import Registry
from . import pages as pages_module
from .font import Glyphs
from .font import build as build_font

logger = logging.getLogger(__name__)

ITEM_ID = "cookbook"
FONT_ID = "recipe_book"


def generate(ctx: Context, registry: Registry) -> None:
    """Build the font and write the pages into the cookbook item."""

    groups = group_recipes(registry)
    glyphs = Glyphs()

    ctx.assets["tasty_supplies"].fonts[FONT_ID] = Font(build_font(ctx, groups, glyphs))

    book = registry.get(ITEM_ID)
    if book is None:
        logger.warning("No %r item in the catalog, skipping the recipe book.", ITEM_ID)
        return

    book.components["written_book_content"]["pages"] = pages_module.build(
        registry, groups, glyphs
    )


def group_recipes(registry: Registry) -> Dict[str, List[RecipeSpec]]:
    """Recipes worth showing, grouped by result, near-duplicates dropped."""

    groups: Dict[str, List[RecipeSpec]] = {}

    for recipe in registry.recipes:
        if recipe.book:
            groups.setdefault(ref_key(recipe.result), []).append(recipe)

    return {key: _unique(recipes) for key, recipes in groups.items() if recipes}


def _unique(recipes: List[RecipeSpec]) -> List[RecipeSpec]:
    """One page per distinct recipe: the three cooking variants share a page."""

    seen = set()
    unique = []
    for recipe in recipes:
        signature = recipe.signature()
        if signature not in seen:
            seen.add(signature)
            unique.append(recipe)
    return unique
