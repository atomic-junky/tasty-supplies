"""Recipes, as plain data turned into JSON at emission time.

A recipe is carried by the item it produces, or declared on its own through
``Recipe``, in which case it names its ``result``.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from .declaration import Declarable
from .item import Item
from .utils import to_absolute_path

Ref = Union[type, Item, str, dict]
BrewingRef = Union[Ref, Tuple[Ref, Optional[str]]]


def as_ingredient(ref: Ref) -> Union[str, dict]:
    """How an ingredient appears in a recipe.

    A vanilla recipe cannot match on components, so a custom item boils down
    to its support (see ``bases.py``).
    """

    if isinstance(ref, Item):
        return to_absolute_path(ref.support.id)
    if isinstance(ref, str):
        return to_absolute_path(ref)
    return ref


def as_result(ref: Ref, count: int = 1) -> Dict[str, Any]:
    if isinstance(ref, Item):
        return ref.stack(count)
    if isinstance(ref, dict):
        return ref
    return {"id": to_absolute_path(str(ref)), "count": count}


def ref_key(ref: Ref) -> str:
    """Stable key of an ingredient or a result, to compare recipes."""

    if isinstance(ref, Item):
        return ref.id
    if isinstance(ref, str):
        identifier = to_absolute_path(ref)
        if identifier.startswith("#"):
            return identifier
        return identifier.removeprefix("minecraft:")
    return repr(ref)


def ref_title(ref: Ref) -> str:
    """Name shown at the top of a cookbook page, or on a tag tooltip."""

    return ref_key(ref).split(":")[-1].replace("_", " ").title()


@dataclass
class RecipeSpec:
    """Base of all recipes. ``result`` and ``id`` are filled by the registry."""

    count: int = 1
    result: Optional[Ref] = None
    id: str = ""
    category: str = "misc"
    ts_category: str = ""
    book: bool = True
    suffix: str = ""
    matches_support = True

    def resolve(self, resolver: Any) -> None:
        """Replace item classes with their instances."""

        self.result = resolver(self.result)

    def ingredients(self) -> List[Ref]:
        return []

    def signature(self) -> tuple:
        """Recipes sharing a signature deserve a single cookbook page."""

        return (type(self).__name__, tuple(ref_key(i) for i in self.ingredients()))

    def duplicate_key(self) -> tuple:
        """Two recipes sharing this key are the very same recipe, twice."""

        return (type(self).__name__, ref_key(self.result), self.count, self.signature())

    def to_json(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    def result_json(self) -> Dict[str, Any]:
        return as_result(self.result, self.count)


@dataclass
class Shaped(RecipeSpec):
    """Crafting recipe with a layout."""

    pattern: List[str] = field(default_factory=list)
    key: Dict[str, Ref] = field(default_factory=dict)

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.key = {char: resolver(ref) for char, ref in self.key.items()}

    def ingredients(self) -> List[Ref]:
        return list(self.key.values())

    def signature(self) -> tuple:
        return (
            "shaped",
            tuple(self.pattern),
            tuple((char, ref_key(ref)) for char, ref in sorted(self.key.items())),
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": "minecraft:crafting_shaped",
            "category": self.category,
            "pattern": self.pattern,
            "key": {char: as_ingredient(ref) for char, ref in self.key.items()},
            "result": self.result_json,
        }


@dataclass
class Shapeless(RecipeSpec):
    """Crafting recipe with no layout."""

    items: List[Ref] = field(default_factory=list)

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.items = [resolver(ref) for ref in self.items]

    def ingredients(self) -> List[Ref]:
        return list(self.items)

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": "minecraft:crafting_shapeless",
            "category": self.category,
            "ingredients": [as_ingredient(ref) for ref in self.items],
            "result": self.result_json,
        }


@dataclass
class Brewing(RecipeSpec):
    """Brewing stand recipe."""

    input: Optional[Ref] = None
    reagent: Optional[Ref] = None
    input_potion: Optional[str] = None
    reagent_potion: Optional[str] = None

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.input_item = resolver(self.input_item)
        self.reagent = resolver(self.reagent)
    
    def ingredients(self) -> List[Ref]:
        return (self.input, self.reagent)

    def to_json(self) -> Dict[str, Any]:
        result: dict = {
            "type": "minecraft:brewing",
            "input": {
                "item": as_ingredient(self.input),
                "potion_content": {},
            },
            "reagent": {
                "item": as_ingredient(self.reagent),
                "potion_content": {},
            },
            "output": self.result_json
        }

        if self.input_potion is not None:
            result["input"]["potion_content"]["id"] = to_absolute_path(self.input_potion)

        if self.reagent_potion is not None:
            result["reagent"]["potion_content"]["id"] = to_absolute_path(self.reagent_potion)

        return result


@dataclass
class Cooking(RecipeSpec):
    """One concrete cooking recipe: furnace, smoker or campfire."""

    ingredient: Optional[Ref] = None
    type: str = "smelting"
    time: int = 200
    xp: float = 0.1

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.ingredient = resolver(self.ingredient)

    def ingredients(self) -> List[Ref]:
        return [self.ingredient]

    def signature(self) -> tuple:
        # The three variants of one cooking recipe deserve a single page.
        return ("cooking", ref_key(self.ingredient))

    def duplicate_key(self) -> tuple:
        return super().duplicate_key() + (self.type,)

    def to_json(self) -> Dict[str, Any]:
        recipe: Dict[str, Any] = {
            "type": f"minecraft:{self.type}",
            "ingredient": as_ingredient(self.ingredient),
            "result": self.result_json,
            "cookingtime": self.time,
        }
        if self.type != "campfire_cooking":
            recipe["experience"] = self.xp
            recipe["category"] = self.category
        return recipe


@dataclass
class Cooked(RecipeSpec):
    """Shorthand: furnace, smoker and campfire in one go."""

    ingredient: Optional[Ref] = None
    time: int = 200
    xp: float = 0.1

    #: Suffix, recipe type, time factor, and whether it grants experience.
    VARIANTS = (
        ("smelting", "smelting", 0.5, True),
        ("smoking", "smoking", 0.5, True),
        ("campfire", "campfire_cooking", 3.0, False),
    )

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.ingredient = resolver(self.ingredient)

    def ingredients(self) -> List[Ref]:
        return [self.ingredient]

    def expand(self) -> List[Cooking]:
        return [
            Cooking(
                count=self.count,
                result=self.result,
                category=self.category,
                ts_category=self.ts_category,
                book=self.book,
                suffix=suffix,
                ingredient=self.ingredient,
                type=cooking_type,
                time=int(self.time * factor),
                xp=self.xp if gives_xp else 0.0,
            )
            for suffix, cooking_type, factor, gives_xp in self.VARIANTS
        ]


@dataclass
class Cut(RecipeSpec):
    """Cutting board recipe (see ``plugins.cutting_board``)."""

    ingredient: Optional[Ref] = None

    # Tests the model data, so it tells custom items apart.
    matches_support = False

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.ingredient = resolver(self.ingredient)

    def ingredients(self) -> List[Ref]:
        return [self.ingredient]

    def to_json(self) -> Dict[str, Any]:
        raise TypeError("A cutting recipe emits functions, not a recipe file.")


@dataclass
class Smithing(RecipeSpec):
    """Smithing table upgrade."""

    template: Ref = "netherite_upgrade_smithing_template"
    base: Optional[Ref] = None
    addition: Optional[Ref] = None

    def resolve(self, resolver: Any) -> None:
        super().resolve(resolver)
        self.template = resolver(self.template)
        self.base = resolver(self.base)
        self.addition = resolver(self.addition)

    def ingredients(self) -> List[Ref]:
        return [self.template, self.base, self.addition]

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": "minecraft:smithing_transform",
            "template": as_ingredient(self.template),
            "base": as_ingredient(self.base),
            "addition": as_ingredient(self.addition),
            "result": self.result_json,
        }


class Recipe(Declarable, abstract=True):
    """A recipe declared on its own, naming the item it produces."""

    result: Ref = ""
    book: bool = True

    def recipes(self) -> List[RecipeSpec]:
        return list(type(self).declaration().recipes)
