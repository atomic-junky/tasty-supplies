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

    def generate(self, ctx: TSContext):
        """Generate workstation items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all workstation items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all workstation recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all workstation items and add them to the bucket."""
        items = [
            # Cutting Board - special BlockItem
            BlockItem(
                "cutting_board",
                base_item="armor_stand",
                custom_data={"tags": ["cutting_board_placer"]},
                entity_data={
                    "id": "minecraft:armor_stand",
                    "Tags": ["cutting_board_placer"],
                    "Invisible": True,
                    "Small": True,
                },
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="workstation")

    def _create_recipes(self):
        """Create all workstation recipes."""
        # Cutting Board Recipe
        self.bucket.add_recipe(
            ShapedRecipe(
                pattern=["spp", "spp"],
                key={"p": "#minecraft:planks", "s": "minecraft:stick"},
                result=self.bucket.get("cutting_board"),
            ),
            category="workstation",
        )

    def register(self, ctx: TSContext):
        """Register workstation with context and generate drop function.

        Args:
            ctx: The Tasty Supplies context
        """
        super().register(ctx)

        # Generate the cutting_board/drop.mcfunction
        cutting_board = self.bucket.get("cutting_board")
        if cutting_board:
            ctx.data["tasty_supplies:cutting_board/drop"] = Function(
                [f"summon minecraft:item ~ ~.5 ~ {{Item:{cutting_board.to_result()}}}"]
            )
