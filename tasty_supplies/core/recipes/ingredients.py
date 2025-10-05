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
