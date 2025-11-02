"""Ingredients category - contains base ingredient items and their recipes.

This module defines raw and processed ingredients used in other recipes.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    Bucket,
    Item,
    AutoCookingRecipe,
    CuttingBoardRecipe,
    ShapedRecipe,
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

    def create_items(self):
        """Create all ingredient items and add them to the bucket."""
        self.add_item(
            Item(
                "butter",
                base_item=aliases.BUTTER,
                food={"nutrition": 2, "saturation": 1.2},
                consumable={"on_consume_effects": [{"type": "clear_all_effects"}]},
            )
        )
        self.add_item(Item("pie_crust", base_item=aliases.PIE_CRUST))
        self.add_item(Item("rice", base_item=aliases.RICE))
        self.add_item(
            Item(
                "cooked_rice",
                base_item=aliases.COOKED_RICE,
                food={"nutrition": 2, "saturation": 3.2},
            )
        )
        self.add_item(
            Item(
                "raw_cod_slice",
                base_item=aliases.RAW_COD_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            )
        )
        self.add_item(
            Item(
                "raw_salmon_slice",
                base_item=aliases.RAW_SALMON_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            )
        )
        self.add_item(
            Item(
                "ice_cream_cone",
                food={"nutrition": 2, "saturation": 0.4},
            )
        )

    def create_recipes(self):
        """Create all ingredient recipes and add them to the bucket."""

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="wheat",
                result=self.bucket.get("rice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            AutoCookingRecipe(
                ingredient=self.bucket.get_ingredient("rice"),
                result=self.bucket.get("cooked_rice"),
                base_cooking_time=150,
                experience=0.25,
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="cod",
                result=self.bucket.get("raw_cod_slice"),
                result_count=2,
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="salmon",
                result=self.bucket.get("raw_salmon_slice"),
                result_count=2,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                key={"W": "wheat"},
                pattern=[["W"], ["W"], ["W"]],
                result=self.bucket.get("ice_cream_cone"),
                result_count=4,
            ),
        )
