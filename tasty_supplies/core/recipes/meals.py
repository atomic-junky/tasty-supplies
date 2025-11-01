from .. import (
    TSContext,
    Bucket,
    Item,
    ShapelessRecipe as NewShapelessRecipe,
    ShapedRecipe as NewShapedRecipe,
    AutoCookingRecipe,
    CuttingBoardRecipe,
    Category,
    aliases,
)


class Meals(Category):
    def __init__(self, bucket: Bucket):
        """Initialize Meals category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Meals", bucket)

    def create_items(self):
        """Create all meal items and add them to the bucket."""
        self.add_item(
            Item(
                "beef_skewer",
                food={"nutrition": 16, "saturation": 25.6},
            )
        )
        self.add_item(
            Item(
                "beef_stew",
                base_item="rabbit_stew",
                food={"nutrition": 10, "saturation": 12},
            )
        )
        self.add_item(Item("cod_roll", food={"nutrition": 7, "saturation": 9.4}))
        self.add_item(Item("cheese", food={"nutrition": 8, "saturation": 5.6}))
        self.add_item(
            Item(
                "cheese_slice",
                food={"nutrition": 2, "saturation": 1.4},
            )
        )
        self.add_item(Item("fried_egg", food={"nutrition": 8, "saturation": 2.4}))
        self.add_item(
            Item(
                "fruit_salad",
                base_item="beetroot_soup",
                food={"nutrition": 18, "saturation": 7.6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:regeneration",
                                    "duration": 600,
                                    "amplifier": 0,
                                }
                            ],
                        }
                    ]
                },
            )
        )
        self.add_item(
            Item(
                "fungus_skewer",
                food={"nutrition": 5, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:nausea",
                                    "duration": 600,
                                    "amplifier": 0,
                                }
                            ],
                        }
                    ]
                },
                use_remainder={"id": "minecraft:stick"},
            )
        )
        self.add_item(
            Item(
                "honey_cookie",
                food={"nutrition": 2, "saturation": 0.4},
            )
        )
        self.add_item(
            Item(
                "ice_cream",
                food={"nutrition": 4, "saturation": 3.6},
                max_stack_size=16,
            )
        )
        self.add_item(
            Item(
                "kelp_roll",
                food={"nutrition": 10, "saturation": 12.6},
            )
        )
        self.add_item(
            Item(
                "kelp_roll_slice",
                food={"nutrition": 2.5, "saturation": 6.2},
            )
        )
        self.add_item(
            Item(
                "melon_popsicle",
                food={"nutrition": 3, "saturation": 0.5},
            )
        )
        self.add_item(
            Item(
                "mushroom_skewer",
                food={"nutrition": 6, "saturation": 7.2},
                use_remainder={"id": "minecraft:stick"},
            )
        )
        self.add_item(
            Item(
                "nether_salad",
                base_item="beetroot_soup",
                food={"nutrition": 5, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:nausea",
                                    "duration": 600,
                                    "amplifier": 0,
                                }
                            ],
                        }
                    ]
                },
            )
        )
        self.add_item(
            Item(
                "potato_fries",
                food={"nutrition": 1.5, "saturation": 1.5},
            )
        )
        self.add_item(
            Item(
                "salmon_roll",
                food={"nutrition": 7, "saturation": 9.4},
            )
        )
        self.add_item(
            Item(
                "stuffed_potato",
                food={"nutrition": 6, "saturation": 7.8},
            )
        )
        self.add_item(
            Item(
                "sweet_berry_cookie",
                food={"nutrition": 2, "saturation": 0.4},
            )
        )
        self.add_item(
            Item(
                "warped_mutton",
                base_item="rabbit_stew",
                food={"nutrition": 6, "saturation": 11},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:nausea",
                                    "duration": 300,
                                    "amplifier": 0,
                                }
                            ],
                        }
                    ]
                },
            )
        )

    def create_recipes(self):
        """Create all meal recipes and add them to the bucket."""

        self.add_recipe(
            NewShapedRecipe(
                pattern=["b", "b", "s"],
                key={"b": "cooked_beef", "s": "stick"},
                result=self.bucket.get("beef_skewer"),
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=["bowl", "cooked_beef", "carrot", "baked_potato"],
                result=self.bucket.get("beef_stew"),
            ),
        )

        self.add_recipe(
            AutoCookingRecipe(
                ingredient="milk_bucket",
                result=self.bucket.get("cheese"),
                base_cooking_time=200,
                experience=0.5,
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("cheese"),
                result=self.bucket.get("cheese_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            AutoCookingRecipe(
                ingredient="#minecraft:eggs",
                result=self.bucket.get("fried_egg"),
                base_cooking_time=140,
                experience=0.1,
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=[
                    "bowl",
                    "apple",
                    "apple",
                    "melon_slice",
                    "melon_slice",
                    "#tasty_supplies:berries",
                    "#tasty_supplies:berries",
                ],
                result=self.bucket.get("fruit_salad"),
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["w", "c", "s"],
                key={"w": "warped_fungus", "c": "crimson_fungus", "s": "stick"},
                result=self.bucket.get("fungus_skewer"),
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["c", "w", "s"],
                key={"w": "warped_fungus", "c": "crimson_fungus", "s": "stick"},
                result=self.bucket.get("fungus_skewer"),
                recipe_id="fungus_skewer_reversed",
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["whw"],
                key={"h": "honey_bottle", "w": "wheat"},
                result=self.bucket.get("honey_cookie"),
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=[
                    "snowball",
                    "sugar",
                    self.bucket.get_ingredient("ice_cream_cone"),
                ],
                result=self.bucket.get("ice_cream"),
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "ice",
                    "ice",
                    "stick",
                ],
                result=self.bucket.get("melon_popsicle"),
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["b", "r", "s"],
                key={"b": "brown_mushroom", "r": "red_mushroom", "s": "stick"},
                result=self.bucket.get("mushroom_skewer"),
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["r", "b", "s"],
                key={"b": "brown_mushroom", "r": "red_mushroom", "s": "stick"},
                result=self.bucket.get("mushroom_skewer"),
                recipe_id="mushroom_skewer_reversed",
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=["bowl", "crimson_fungus", "warped_fungus"],
                result=self.bucket.get("nether_salad"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="baked_potato",
                result=self.bucket.get("potato_fries"),
                result_count=4,
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["wbw"],
                key={"b": "sweet_berries", "w": "wheat"},
                result=self.bucket.get("sweet_berry_cookie"),
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=["baked_potato", "cooked_beef", "carrot", "milk_bucket"],
                result=self.bucket.get("stuffed_potato"),
            ),
        )

        self.add_recipe(
            NewShapelessRecipe(
                ingredients=["warped_roots", "warped_roots", "bowl", "cooked_mutton"],
                result=self.bucket.get("warped_mutton"),
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["rcr", "kkk"],
                key={
                    "k": "dried_kelp",
                    "r": self.bucket.get_ingredient("cooked_rice"),
                    "c": "carrot",
                },
                result=self.bucket.get("kelp_roll"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("kelp_roll"),
                result=self.bucket.get("kelp_roll_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["s", "s", "r"],
                key={
                    "s": self.bucket.get_ingredient("raw_salmon_slice"),
                    "r": self.bucket.get_ingredient("cooked_rice"),
                },
                result=self.bucket.get("salmon_roll"),
                result_count=2,
            ),
        )

        self.add_recipe(
            NewShapedRecipe(
                pattern=["c", "c", "r"],
                key={
                    "c": self.bucket.get_ingredient("raw_cod_slice"),
                    "r": self.bucket.get_ingredient("cooked_rice"),
                },
                result=self.bucket.get("cod_roll"),
                result_count=2,
            ),
        )
