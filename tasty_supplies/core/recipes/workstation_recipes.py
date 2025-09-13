from .. import (
    TSContext,
    BlockItem,
    ShapedRecipe,
    Result,
    Category,
)


class WorksationCategory(Category):
    def __init__(self):
        super().__init__("Workstation")

    def generate(self, ctx: TSContext):
        BlockItem(
            "cutting_board",
            ShapedRecipe(
                key={"p": "#minecraft:planks", "s": "minecraft:stick"},
                pattern=["spp", "spp"],
                result=Result(
                    count=1,
                    max_stack_size=64,
                    extra_components={
                        "custom_data": {"tags": ["cutting_board_placer"]},
                        "entity_data": {
                            "id": "minecraft:armor_stand",
                            "Tags": ["cutting_board_placer"],
                            "Invisible": 1,
                            "Small": 1,
                        },
                    },
                ),
            ),
        ).register(ctx)
