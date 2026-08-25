"""Tasty Supplies: the generator behind the data pack and the resource pack.

``ts.catalog`` holds the content, ``ts.declare`` the decorators it uses,
``ts.plugins`` the steps of the build.
"""

from . import bases
from .bases import Base
from .declare import (
    apply_effect,
    component,
    consume_effect,
    cooked,
    cooldown,
    cut,
    disable,
    food,
    potion_effect,
    rarity,
    remainder,
    shaped,
    shapeless,
    smithing,
    stack,
)
from .item import Item
from .recipe import Cooked, Cooking, Cut, Recipe, Shaped, Shapeless, Smithing

__all__ = [
    "Base",
    "Item",
    "Recipe",
    "bases",
    # recipe kinds, for the rare case a family builds one by hand
    "Cooked",
    "Cooking",
    "Cut",
    "Shaped",
    "Shapeless",
    "Smithing",
    # decorators
    "apply_effect",
    "component",
    "consume_effect",
    "cooked",
    "cooldown",
    "cut",
    "disable",
    "food",
    "potion_effect",
    "rarity",
    "remainder",
    "shaped",
    "shapeless",
    "smithing",
    "stack",
]
