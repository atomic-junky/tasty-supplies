from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bucket import Bucket
    from .item import Item

from . import TSContext


class Category:
    """Base class for item and recipe categories.

    Categories organize items and recipes into logical groups,
    automatically tagging them for easier management.
    """

    def __init__(self, category_name: str = "", bucket: Optional["Bucket"] = None):
        """Initialize a category.

        Args:
            category_name: Name of the category (e.g., "Meals", "Tools")
            bucket: Bucket instance to store items and recipes
        """
        self.category_name = category_name
        self.bucket: Optional["Bucket"] = bucket

    def add_item(self, item: "Item", category: str = "misc") -> None:
        """Add an item to the bucket.

        Args:
            item: The Item instance to add
        """
        if self.bucket is None:
            raise ValueError("Bucket is not initialized for this category")
        self.bucket.add_item(item, category)

    def add_recipe(self, recipe) -> None:
        """Add a recipe with automatic category tagging.

        Args:
            recipe: The recipe instance to add
        """
        if self.bucket is None:
            raise ValueError("Bucket is not initialized for this category")
        self.bucket.add_recipe(recipe, category=self.category_name.lower())

    def create_items(self):
        """Create all items for this category."""
        pass

    def create_recipes(self):
        """Create all recipes for this category."""
        pass
