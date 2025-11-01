from ..bucket import Bucket
from . import TSContext


class Category:
    def __init__(self, category_name="", bucket=None):
        self.category_name = category_name
        self.bucket: Bucket = bucket

    def add_item(self, item):
        """Add an item with automatic category tagging."""
        self.bucket.add_item(item, category=self.category_name.lower())

    def add_recipe(self, recipe):
        """Add a recipe with automatic category tagging."""
        self.bucket.add_recipe(recipe, category=self.category_name.lower())

    def create_items(self):
        """Create all items for this category."""
        pass

    def create_recipes(self):
        """Create all recipes for this category."""
        pass
