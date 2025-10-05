from .. import (
    TSContext,
    Item,
    ShapelessRecipe,
    ShapedRecipe,
    AutoBakeRecipe,
    CuttingBoardRecipe,
    Result,
    FoodResult,
    Effect,
    Category,
    FoodSliceResult,
    aliases,
)


class Ingredients(Category):
    def generate(self, ctx: TSContext):
        Item(
            "rice",
            CuttingBoardRecipe("wheat", result=Result(count=4)),
            base_item=aliases.RICE,
        ).register(ctx)

        Item(
            "cooked_rice",
            AutoBakeRecipe(
                aliases.RICE, 0.25, 150, result=FoodResult(nutrition=2, saturation=3.2)
            ),
            base_item=aliases.COOKED_RICE,
        ).register(ctx)

        Item(
            "raw_cod_slice",
            CuttingBoardRecipe(
                "cod", result=FoodResult(count=2, nutrition=1, saturation=0.8)
            ),
            base_item=aliases.RAW_COD_SLICE,
        ).register(ctx)

        Item(
            "raw_salmon_slice",
            CuttingBoardRecipe(
                "salmon", result=FoodResult(count=2, nutrition=1, saturation=0.8)
            ),
            base_item=aliases.RAW_SALMON_SLICE,
        ).register(ctx)
