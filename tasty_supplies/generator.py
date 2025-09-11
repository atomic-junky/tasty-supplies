from lib import *


def generate(ctx: TSContext):
    log.info("Generating items...")

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
        "apple_pie",
        ShapedRecipe(
            key={"W": "wheat", "A": "apple", "S": "sugar", "C": "bread"},
            pattern=["WWW", "AAA", "SCS"],
            result=FoodResult(nutrition=8, saturation=6),
        ),
        base_item="bread",
    ).register(ctx)

    Item("apple_pie_slice").register(ctx)

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
        "cheese",
        AutoBakeRecipe(
            ingredient="milk_bucket",
            experience=0.5,
            cookingtime=200,
            result=FoodResult(nutrition=8, saturation=5.6),
        ),
    ).register(ctx)

    Item("cheese_slice").register(ctx)

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

    Item("chocolate_pie_slice").register(ctx)

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

    knife_pattern = ["m", "s"]

    def knife_shape(m: str):
        return {"m": f"minecraft:{m}", "s": "minecraft:stick"}

    def knife_attr(damage: float, speed: float, id_prefix: str):
        return [
            {
                "type": "attack_damage",
                "slot": "mainhand",
                "id": f"tasty_supplies:{id_prefix}_knife_damage",
                "amount": damage,
                "operation": "add_value",
            },
            {
                "type": "attack_speed",
                "slot": "mainhand",
                "id": f"tasty_supplies:{id_prefix}_knife_speed",
                "amount": speed,
                "operation": "add_value",
            },
        ]

    Item(
        "netherite_knife",
        ShapedRecipe(
            key=knife_shape("netherite_ingot"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 2032,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(4.5, 2, "netherite"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "diamond_knife",
        ShapedRecipe(
            key=knife_shape("diamond"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 1561,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(4, 2, "diamond"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "golden_knife",
        ShapedRecipe(
            key=knife_shape("gold_ingot"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 32,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(2, 2, "golden"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "iron_knife",
        ShapedRecipe(
            key=knife_shape("iron_ingot"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 250,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(3.5, 2, "iron"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "copper_knife",
        ShapedRecipe(
            key=knife_shape("copper_ingot"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 190,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(3, 2, "copper"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "flint_knife",
        ShapedRecipe(
            key=knife_shape("flint"),
            pattern=knife_pattern,
            category="equipement",
            result=Result(
                extra_components={
                    "max_damage": 131,
                    "weapon": {},
                    "attribute_modifiers": knife_attr(2, 2, "flint"),
                }
            ),
        ),
        base_item="wooden_hoe",
    ).register(ctx)

    Item(
        "fried_egg",
        AutoBakeRecipe(
            ingredient="#eggs",
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
        "glow_berry_custard_horn",
        ShapelessRecipe(
            ingredients=["glow_berries", "milk_bucket", "egg", "sugar", "goat_horn"],
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

    Item(
        "glow_berry_custard",
        ShapelessRecipe(
            ingredients=["glow_berries", "milk_bucket", "egg", "sugar", "glass_bottle"],
            result=PotionResult(
                max_stack_size=1, potion_effects=[Effect("glowing", 3600)]
            ),
        ),
        base_item="potion",
    ).register(ctx)

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

    Item("glow_berry_pie_slice").register(ctx)

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
        "pie_crust", ShapedRecipe(key={"W": "minecraft:wheat"}, pattern=["W W", " W "])
    ).register(ctx)

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

    Item("sweet_berry_cheesecake_slice").register(ctx)

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

    log.info(f"Items generated")
    log.info(f"\t- {len(ctx.data.recipes)} recipes")
