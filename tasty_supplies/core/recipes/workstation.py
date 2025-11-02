from beet import Function
from .. import (
    TSContext,
    Item,
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
            Item(
                item_name="cutting_board",
                base_item="armor_stand",
                texture_path="tasty_supplies:block/cutting_board",
                model_type="block",
                max_stack_size=64,
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
