from beet import Function
from .. import (
    TSContext,
    BlockItem,
    ShapedRecipe,
    Result,
    Category,
)


class Worksation(Category):
    def __init__(self):
        super().__init__("Workstation")

    def generate(self, ctx: TSContext):
        cutting_board_item: BlockItem = BlockItem(
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
                            "Invisible": True,
                            "Small": True,
                        },
                    },
                ),
            ),
        )

        ctx.data["tasty_supplies:cutting_board/drop"] = Function(
            [
                "summon minecraft:item ~ ~.5 ~ {Item:%s}"
                % cutting_board_item.recipe.result._to_json(
                    cutting_board_item.name, cutting_board_item.base_item
                )
            ]
        )

        cutting_board_item.register(ctx)
