from .. import (
    TSContext,
    Item,
    ShapelessRecipe,
    ShapedRecipe,
    FoodSliceResult,
    CuttingBoardRecipe,
    AutoBakeRecipe,
    Effect,
    Category,
    FoodResult,
    aliases,
)


class Sweets(Category):
    def __init__(self):
        super().__init__("Sweets")

    def generate(self, ctx: TSContext):
        ## Butter

        Item(
            "butter",
            ShapelessRecipe(
                ingredients=["milk_bucket"],
                result=FoodResult(
                    nutrition=2, saturation=1.2, consume_effect_type="clear_all_effects"
                ),
            ),
            base_item=aliases.BUTTER,
        ).register(ctx)

        ## Pie Crust

        Item(
            "pie_crust",
            ShapedRecipe(
                key={"W": "minecraft:wheat", "B": aliases.BUTTER},
                pattern=["WBW", " W "],
            ),
            base_item=aliases.PIE_CRUST,
        ).register(ctx)

        ## Apple Pie

        Item(
            "apple_pie",
            ShapedRecipe(
                key={"W": "wheat", "A": "apple", "S": "sugar", "B": aliases.PIE_CRUST},
                pattern=["WWW", "AAA", "SBS"],
                result=FoodResult(nutrition=8, saturation=6),
            ),
            base_item="bread",
        ).register(ctx)

        Item(
            "apple_pie_slice",
            CuttingBoardRecipe(
                "apple_pie", FoodSliceResult(nutrition=2, saturation=1.5)
            ),
        ).register(ctx)

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

        Item(
            "cheese_slice",
            CuttingBoardRecipe("cheese", FoodSliceResult(nutrition=2, saturation=1.4)),
        ).register(ctx)

        ## Cherry Blossom Pie

        Item(
            "cherry_blossom_pie",
            ShapedRecipe(
                key={
                    "C": "minecraft:cherry_leaves",
                    "M": "minecraft:milk_bucket",
                    "H": "minecraft:honeycomb",
                    "B": aliases.PIE_CRUST,
                },
                pattern=["CCC", "MMM", "HBH"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("slow_falling", 3600, 1)]
                ),
            ),
        ).register(ctx)

        Item(
            "cherry_blossom_pie_slice",
            CuttingBoardRecipe(
                "cherry_blossom_pie",
                FoodSliceResult(
                    nutrition=2,
                    saturation=1.5,
                    effects=[Effect("slow_falling", 900, 1)],
                ),
            ),
        ).register(ctx)

        ## Chocolate Pie

        Item(
            "chocolate_pie",
            ShapedRecipe(
                key={
                    "C": "minecraft:cocoa_beans",
                    "M": "minecraft:milk_bucket",
                    "S": "minecraft:sugar",
                    "B": aliases.PIE_CRUST,
                },
                pattern=["CCC", "MMM", "SBS"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("speed", 3600, 1)]
                ),
            ),
        ).register(ctx)

        Item(
            "chocolate_pie_slice",
            CuttingBoardRecipe(
                "chocolate_pie",
                FoodSliceResult(
                    nutrition=2, saturation=1.5, effects=[Effect("speed", 900, 1)]
                ),
            ),
        ).register(ctx)

        ## Chorus Pie

        Item(
            "chorus_pie",
            ShapedRecipe(
                key={
                    "C": "minecraft:chorus_fruit",
                    "M": "minecraft:milk_bucket",
                    "S": "minecraft:sugar",
                    "P": aliases.PIE_CRUST,
                },
                pattern=["CCC", "SSS", "MPM"],
                result=FoodResult(
                    nutrition=8,
                    saturation=6,
                    consume_effect_type="teleport_randomly",
                    consume_effect_diameter=32,
                    extra_components={
                        "use_cooldown": {"seconds": 2.0, "cooldown_group": "chorus_pie"}
                    },
                ),
            ),
        ).register(ctx)

        Item(
            "chorus_pie_slice",
            CuttingBoardRecipe(
                "chorus_pie",
                FoodSliceResult(
                    nutrition=2,
                    saturation=1.5,
                    consume_effect_type="teleport_randomly",
                    consume_effect_diameter=8,
                    extra_components={
                        "use_cooldown": {"seconds": 1.0, "cooldown_group": "chorus_pie"}
                    },
                ),
            ),
        ).register(ctx)

        ## Glow Berry Pie

        Item(
            "glow_berry_pie",
            ShapedRecipe(
                key={
                    "G": "minecraft:glow_berries",
                    "M": "minecraft:milk_bucket",
                    "S": "minecraft:sugar",
                    "B": aliases.PIE_CRUST,
                },
                pattern=["GGG", "SSS", "MBM"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("glowing", 3600)]
                ),
            ),
        ).register(ctx)

        Item(
            "glow_berry_pie_slice",
            CuttingBoardRecipe(
                "glow_berry_pie",
                FoodSliceResult(
                    nutrition=2, saturation=1.5, effects=[Effect("glowing", 900, 1)]
                ),
            ),
        ).register(ctx)

        ## Sweet Berry Cheesecake

        Item(
            "sweet_berry_cheesecake",
            ShapedRecipe(
                key={
                    "S": "minecraft:sweet_berries",
                    "M": "minecraft:milk_bucket",
                    "B": aliases.PIE_CRUST,
                },
                pattern=["SSS", "SSS", "MBM"],
                result=FoodResult(
                    nutrition=8, saturation=6, effects=[Effect("speed", 3600)]
                ),
            ),
        ).register(ctx)

        Item(
            "sweet_berry_cheesecake_slice",
            CuttingBoardRecipe(
                "sweet_berry_cheesecake",
                FoodSliceResult(
                    nutrition=2, saturation=1.5, effects=[Effect("speed", 900, 1)]
                ),
            ),
        ).register(ctx)

        ## Croissant

        Item(
            "croissant",
            ShapedRecipe(
                key={
                    "W": "minecraft:wheat",
                    "B": aliases.BUTTER,
                    "S": "minecraft:sugar",
                },
                pattern=["WBS", "WBS"],
                result=FoodResult(nutrition=6, saturation=3.4),
            ),
        ).register(ctx)

        ## Honeyed Apple

        Item(
            "honeyed_apple",
            ShapelessRecipe(
                ingredients=[
                    "minecraft:apple",
                    "minecraft:honey_bottle",
                ],
                result=FoodResult(nutrition=6, saturation=8.6),
            ),
        ).register(ctx)

        ## Sweet Roll

        Item(
            "sweet_roll",
            ShapelessRecipe(
                ingredients=[
                    "minecraft:wheat",
                    "minecraft:sugar",
                    "#minecraft:eggs",
                    aliases.BUTTER,
                ],
                result=FoodResult(nutrition=8, saturation=12.8),
            ),
        ).register(ctx)
