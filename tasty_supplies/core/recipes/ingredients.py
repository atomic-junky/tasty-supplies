"""Ingredients category - contains base ingredient items and their recipes.

This module defines raw and processed ingredients used in other recipes.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    TSContext,
    Bucket,
    Item,
    AutoCookingRecipe,
    CuttingBoardRecipe,
    Category,
    aliases,
)


class Ingredients(Category):
    """Category for ingredient items."""

    def __init__(self, bucket: Bucket):
        """Initialize Ingredients category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Ingredients", bucket)

    def generate(self, ctx: TSContext):
        """Generate all ingredient items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all ingredient items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all ingredient recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all ingredient items and add them to the bucket."""
        items = [
            # Rice
            Item("rice", base_item=aliases.RICE),
            # Cooked Rice
            Item(
                "cooked_rice",
                base_item=aliases.COOKED_RICE,
                food={"nutrition": 2, "saturation": 3.2},
            ),
            # Raw Cod Slice
            Item(
                "raw_cod_slice",
                base_item=aliases.RAW_COD_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            ),
            # Raw Salmon Slice
            Item(
                "raw_salmon_slice",
                base_item=aliases.RAW_SALMON_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="ingredients")

    def _create_recipes(self):
        """Create all ingredient recipes and add them to the bucket."""

        # Rice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient="wheat",
                result=self.bucket.get("rice"),
                result_count=4,
            ),
            category="ingredients",
        )

        # Cooked Rice
        self.bucket.add_recipe(
            AutoCookingRecipe(
                ingredient=self.bucket.get_ingredient("rice"),
                result=self.bucket.get("cooked_rice"),
                base_cooking_time=150,
                experience=0.25,
            ),
            category="ingredients",
        )

        # Raw Cod Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient="cod",
                result=self.bucket.get("raw_cod_slice"),
                result_count=2,
            ),
            category="ingredients",
        )

        # Raw Salmon Slice (cutting board from salmon)
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient="salmon",
                result=self.bucket.get("raw_salmon_slice"),
                result_count=2,
            ),
            category="ingredients",
        )
