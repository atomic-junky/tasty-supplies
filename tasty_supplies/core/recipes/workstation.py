from beet import Function
from .. import (
    TSContext,
    BlockItem,
    ShapedRecipe,
    Category,
    Bucket,
)


class Worksation(Category):
    """Category for workstation items (cutting board, etc.)."""

    def __init__(self, bucket: Bucket):
        """Initialize Workstation category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Workstation", bucket)

    def create_items(self):
        """Create all workstation items and add them to the bucket."""
        self.add_item(
            BlockItem(
                "cutting_board",
                alias="Oak Cutting Board",
                base_item="minecraft:oak_pressure_plate",
                max_stack_size=64,
                placed_block="minecraft:oak_pressure_plate",
                item_model="tasty_supplies:cutting_board",
            )
        )

    def create_recipes(self):
        """Create all workstation recipes."""
        self.add_recipe(
            ShapedRecipe(
                pattern=["spp", "spp"],
                key={"p": "#minecraft:planks", "s": "minecraft:stick"},
                result=self.bucket.get("cutting_board"),
            ),
        )
