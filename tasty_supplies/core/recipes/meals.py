from .. import (
    TSContext,
    Item,
    ShapelessRecipe,
    ShapedRecipe,
    AutoBakeRecipe,
    CuttingBoardRecipe,
    FoodResult,
    Effect,
    Category,
    FoodSliceResult,
)


class Meals(Category):
    def generate(self, ctx: TSContext):
        Item(
            "beef_skewer",
            ShapedRecipe(
                key={"b": "cooked_beef", "s": "stick"},
                pattern=["b", "b", "s"],
                result=FoodResult(nutrition=16, saturation=25.6),
            ),
        ).register(ctx)

        Item(
            "beef_stew",
            ShapelessRecipe(
                ingredients=["bowl", "cooked_beef", "carrot", "baked_potato"],
                result=FoodResult(nutrition=10, saturation=12),
            ),
            base_item="rabbit_stew",
        ).register(ctx)

        Item(
            "fried_egg",
            AutoBakeRecipe(
                ingredient="#minecraft:eggs",
                experience=0.1,
                cookingtime=140,
                result=FoodResult(nutrition=8, saturation=2.4),
            ),
        ).register(ctx)

        Item(
            "fruit_salad",
            ShapelessRecipe(
                ingredients=[
                    "bowl",
                    "apple",
                    "apple",
                    "melon_slice",
                    "melon_slice",
                    "#tasty_supplies:berries",
                    "#tasty_supplies:berries",
                ],
                result=FoodResult(
                    nutrition=18,
                    saturation=7.6,
                    effects=[Effect("regeneration", 600)],
                ),
            ),
            base_item="beetroot_soup",
        ).register(ctx)

        fungus_skewer_recipe = ShapedRecipe(
            key={
                "w": "minecraft:warped_fungus",
                "c": "minecraft:crimson_fungus",
                "s": "minecraft:stick",
            },
            pattern=["w", "c", "s"],
            result=FoodResult(
                nutrition=5,
                saturation=6,
                effects=[Effect("nausea", 600)],
                extra_components={
                    "use_remainder": {
                        "id": "minecraft:stick",
                    }
                },
            ),
        )

        Item("fungus_skewer", fungus_skewer_recipe).register(ctx)

        fungus_skewer_recipe.pattern = ["c", "w", "s"]
        fungus_skewer_recipe.suffix = "_reversed"
        Item("fungus_skewer", fungus_skewer_recipe).register(ctx)

        Item(
            "honey_cookie",
            ShapedRecipe(
                key={
                    "h": "minecraft:honey_bottle",
                    "w": "minecraft:wheat",
                },
                pattern=["whw"],
                result=FoodResult(nutrition=2, saturation=0.4),
            ),
        ).register(ctx)

        Item(
            "ice_cream_cone",
            ShapedRecipe(
                key={"W": "minecraft:wheat"},
                pattern=["W", "W", "W"],
                result=FoodResult(nutrition=2, saturation=0.4),
            ),
        ).register(ctx)

        Item(
            "ice_cream",
            ShapelessRecipe(
                ingredients=["snowball", "sugar", "bread"],
                result=FoodResult(nutrition=4, saturation=3.6, max_stack_size=16),
            ),
        ).register(ctx)

        Item(
            "melon_popsicle",
            ShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "ice",
                    "ice",
                    "stick",
                ],
                result=FoodResult(nutrition=3, saturation=0.5),
            ),
        ).register(ctx)

        mushroom_skewer_recipe = ShapedRecipe(
            key={
                "b": "minecraft:brown_mushroom",
                "r": "minecraft:red_mushroom",
                "s": "minecraft:stick",
            },
            pattern=["b", "r", "s"],
            result=FoodResult(
                nutrition=6,
                saturation=7.2,
                extra_components={
                    "use_remainder": {
                        "id": "minecraft:stick",
                    }
                },
            ),
        )

        Item("mushroom_skewer", mushroom_skewer_recipe).register(ctx)

        mushroom_skewer_recipe.pattern = ["r", "b", "s"]
        mushroom_skewer_recipe.suffix = "_reversed"
        Item("mushroom_skewer", mushroom_skewer_recipe).register(ctx)

        Item(
            "nether_salad",
            ShapelessRecipe(
                ingredients=["bowl", "crimson_fungus", "warped_fungus"],
                result=FoodResult(
                    nutrition=5, saturation=6, effects=[Effect("nausea", 600)]
                ),
            ),
            base_item="beetroot_soup",
        ).register(ctx)

        Item(
            "potato_fries",
            CuttingBoardRecipe(
                "baked_potato", FoodSliceResult(nutrition=1.5, saturation=1.5)
            ),
        ).register(ctx)

        Item(
            "sweet_berry_cookie",
            ShapedRecipe(
                key={
                    "b": "minecraft:sweet_berries",
                    "w": "minecraft:wheat",
                },
                pattern=["wbw"],
                result=FoodResult(nutrition=2, saturation=0.4),
            ),
        ).register(ctx)

        Item(
            "warped_mutton",
            ShapelessRecipe(
                ingredients=["warped_roots", "warped_roots", "bowl", "cooked_mutton"],
                result=FoodResult(
                    nutrition=6, saturation=11, effects=[Effect("nausea", 300)]
                ),
            ),
            base_item="rabbit_stew",
        ).register(ctx)
