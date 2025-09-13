from .. import (
    TSContext,
    Item,
    ShapedRecipe,
    AutoBakeRecipe,
    CuttingBoardRecipe,
    FoodResult,
    Effect,
    Category,
)


class PieCategory(Category):
    def __init__(self):
        super().__init__("Pie")

    def generate(self, ctx: TSContext):
        ## Apple Pie

        Item(
            "apple_pie",
            ShapedRecipe(
                key={"W": "wheat", "A": "apple", "S": "sugar", "C": "bread"},
                pattern=["WWW", "AAA", "SCS"],
                result=FoodResult(nutrition=8, saturation=6),
            ),
            base_item="bread",
        ).register(ctx)

        Item("apple_pie_slice", CuttingBoardRecipe("apple_pie")).register(ctx)

        ## Cheese

        Item(
            "cheese",
            AutoBakeRecipe(
                ingredient="milk_bucket",
                experience=0.5,
                cookingtime=200,
                result=FoodResult(nutrition=8, saturation=5.6),
            ),
        ).register(ctx)

        Item("cheese_slice", CuttingBoardRecipe("cheese")).register(ctx)

        ## Cherry Blossom Pie

        Item(
            "cherry_blossom_pie",
            ShapedRecipe(
                key={
                    "C": "minecraft:cherry_leaves",
                    "M": "minecraft:milk_bucket",
                    "H": "minecraft:honeycomb",
                    "B": "minecraft:bread",
                },
                pattern=["CCC", "MMM", "HBH"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("slow_falling", 3600, 1)]
                ),
            ),
        ).register(ctx)

        Item(
            "cherry_blossom_pie_slice", CuttingBoardRecipe("cherry_blossom_pie")
        ).register(ctx)

        ## Chocolate Pie

        Item(
            "chocolate_pie",
            ShapedRecipe(
                key={
                    "C": "minecraft:cocoa_beans",
                    "M": "minecraft:milk_bucket",
                    "S": "minecraft:sugar",
                    "B": "minecraft:bread",
                },
                pattern=["CCC", "MMM", "SBS"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("speed", 3600, 1)]
                ),
            ),
        ).register(ctx)

        Item("chocolate_pie_slice", CuttingBoardRecipe("chocolate_pie")).register(ctx)

        ## Glow Berry Pie

        Item(
            "glow_berry_pie",
            ShapedRecipe(
                key={
                    "G": "minecraft:glow_berries",
                    "M": "minecraft:milk_bucket",
                    "S": "minecraft:sugar",
                    "C": "minecraft:bread",
                },
                pattern=["GGG", "SSS", "MCM"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("glowing", 3600)]
                ),
            ),
        ).register(ctx)

        Item("glow_berry_pie_slice", CuttingBoardRecipe("glow_berry_pie")).register(ctx)

        ## Sweet Berry Cheesecake

        Item(
            "sweet_berry_cheesecake",
            ShapedRecipe(
                key={
                    "S": "minecraft:sweet_berries",
                    "M": "minecraft:milk_bucket",
                    "C": "minecraft:bread",
                },
                pattern=["SSS", "SSS", "MCM"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("speed", 3600)]
                ),
            ),
        ).register(ctx)

        Item(
            "sweet_berry_cheesecake_slice", CuttingBoardRecipe("sweet_berry_cheesecake")
        ).register(ctx)

        ## Pie Crust

        Item(
            "pie_crust",
            ShapedRecipe(key={"W": "minecraft:wheat"}, pattern=["W W", " W "]),
            base_item="bread",
        ).register(ctx)
