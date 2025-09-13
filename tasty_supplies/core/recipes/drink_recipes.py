from .. import (
    TSContext,
    Item,
    ShapelessRecipe,
    PotionResult,
    Effect,
    Category,
    FoodResult,
)


class DrinkCategory(Category):
    def __init__(self):
        super().__init__("Drinks")

    def generate(self, ctx: TSContext):
        ## Apple Cider

        Item(
            "apple_cider",
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "glass_bottle"],
                result=PotionResult(
                    max_stack_size=1,
                    potion_effects=[Effect("absorption", 1800, 1)],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:goat_horn",
                        }
                    },
                ),
            ),
            base_item="potion",
        ).register(ctx)

        Item(
            "apple_cider_horn",
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "goat_horn"],
                result=PotionResult(
                    max_stack_size=1,
                    potion_effects=[Effect("absorption", 1800, 1)],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:goat_horn",
                        }
                    },
                ),
            ),
            base_item="potion",
        ).register(ctx)

        ## Glow Berry Custard

        Item(
            "glow_berry_custard",
            ShapelessRecipe(
                ingredients=[
                    "glow_berries",
                    "milk_bucket",
                    "egg",
                    "sugar",
                    "glass_bottle",
                ],
                result=PotionResult(
                    max_stack_size=1, potion_effects=[Effect("glowing", 3600)]
                ),
            ),
            base_item="potion",
        ).register(ctx)

        Item(
            "glow_berry_custard_horn",
            ShapelessRecipe(
                ingredients=[
                    "glow_berries",
                    "milk_bucket",
                    "egg",
                    "sugar",
                    "goat_horn",
                ],
                result=PotionResult(
                    max_stack_size=1,
                    potion_effects=[Effect("glowing", 3600)],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:goat_horn",
                        }
                    },
                ),
            ),
            base_item="potion",
        ).register(ctx)

        ## Hot Cocoa

        Item(
            "hot_cocoa",
            ShapelessRecipe(
                ingredients=[
                    "cocoa_beans",
                    "cocoa_beans",
                    "milk_bucket",
                    "sugar",
                    "glass_bottle",
                ],
                result=PotionResult(
                    max_stack_size=1, potion_effects=[Effect("regeneration", 600)]
                ),
            ),
            base_item="potion",
        ).register(ctx)

        Item(
            "hot_cocoa_horn",
            ShapelessRecipe(
                ingredients=[
                    "cocoa_beans",
                    "cocoa_beans",
                    "milk_bucket",
                    "sugar",
                    "goat_horn",
                ],
                result=PotionResult(
                    max_stack_size=1,
                    potion_effects=[Effect("regeneration", 600)],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:goat_horn",
                        }
                    },
                ),
            ),
            base_item="potion",
        ).register(ctx)

        ## Melon Juice

        Item(
            "melon_juice",
            ShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "sugar",
                    "glass_bottle",
                ],
                result=PotionResult(
                    max_stack_size=1, potion_effects=[Effect("instant_health")]
                ),
            ),
            base_item="potion",
        ).register(ctx)

        Item(
            "melon_juice_horn",
            ShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "sugar",
                    "goat_horn",
                ],
                result=PotionResult(
                    max_stack_size=1,
                    potion_effects=[Effect("instant_health")],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:goat_horn",
                        }
                    },
                ),
            ),
            base_item="potion",
        ).register(ctx)

        ## Magma Gelatin

        Item(
            "magma_gelatin",
            ShapelessRecipe(
                ingredients=[
                    "bucket",
                    "magma_cream",
                    "magma_cream",
                    "magma_cream",
                    "blaze_powder",
                    "blaze_powder",
                ],
                result=FoodResult(
                    nutrition=1,
                    saturation=6,
                    max_stack_size=1,
                    can_always_eat=True,
                    effects=[Effect("nausea", 300), Effect("fire_resistance", 6000)],
                    extra_components={
                        "use_remainder": {
                            "id": "minecraft:bucket",
                        }
                    },
                ),
            ),
        ).register(ctx)
