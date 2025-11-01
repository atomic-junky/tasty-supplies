from ..bucket import Bucket
from . import TSContext


class Category:
    def __init__(self, category_name="", bucket=None):
        self.category_name = category_name
        self.bucket: Bucket = bucket

    def register(self, ctx: TSContext):
        self.generate(ctx)
        ctx.showcase_items.append("\n")

    def generate(self, ctx: TSContext):
        pass

    def create_items(self):
        """Phase 1: Create all items for this category.

        Should call _create_items() if the category has items to create.
        """
        pass

    def create_recipes(self):
        """Phase 2: Create all recipes for this category.

        Should call _create_recipes() if the category has recipes to create.
        Called after all items from all categories have been created.
        """
        pass
