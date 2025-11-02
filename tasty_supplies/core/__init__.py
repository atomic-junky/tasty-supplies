"""Core module for Tasty Supplies datapack generator.

This module provides the main classes and utilities for generating
Minecraft datapacks with custom items and recipes.
"""

from .logger import get_logger, log
from .utils import to_absolute_path
from .bucket import Bucket
from .constants import (
    MINECRAFT_NAMESPACE,
    TASTY_SUPPLIES_NAMESPACE,
    DEFAULT_MAX_STACK_SIZE,
    DEFAULT_BASE_ITEM,
)

from .models.context import TSContext
from .models.item import Item, BlockItem
from .models.category import Category
from .models.recipe import (
    Recipe,
    ShapelessRecipe,
    ShapedRecipe,
    SmeltingRecipe,
    AutoCookingRecipe,
    SmithingTransformRecipe,
    CuttingBoardRecipe,
)

from .aliases import *

__all__ = [
    # Logger
    "get_logger",
    "log",
    # Utils
    "to_absolute_path",
    # Bucket
    "Bucket",
    # Constants
    "MINECRAFT_NAMESPACE",
    "TASTY_SUPPLIES_NAMESPACE",
    "DEFAULT_MAX_STACK_SIZE",
    "DEFAULT_BASE_ITEM",
    # Models
    "TSContext",
    "Item",
    "BlockItem",
    "Category",
    # Recipes
    "Recipe",
    "ShapelessRecipe",
    "ShapedRecipe",
    "SmeltingRecipe",
    "AutoCookingRecipe",
    "SmithingTransformRecipe",
    "CuttingBoardRecipe",
]
