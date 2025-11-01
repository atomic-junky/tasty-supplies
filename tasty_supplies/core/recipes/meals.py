from .. import (
    TSContext,
    Bucket,
    Item,
    ShapelessRecipe as NewShapelessRecipe,
    ShapedRecipe as NewShapedRecipe,
    AutoCookingRecipe,
    CuttingBoardRecipe as NewCuttingBoardRecipe,
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

    def generate(self, ctx: TSContext):
        """Generate all meal items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all meal items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all meal recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all meal items and add them to the bucket."""
        items = [
            Item(
                "beef_skewer",
                base_item="bread",
                food={"nutrition": 16, "saturation": 25.6},
            ),
            Item(
                "beef_stew",
                base_item="rabbit_stew",
                food={"nutrition": 10, "saturation": 12},
            ),
            Item(
                "cod_roll", base_item="bread", food={"nutrition": 7, "saturation": 9.4}
            ),
            Item(
                "fried_egg", base_item="bread", food={"nutrition": 8, "saturation": 2.4}
            ),
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
            ),
            Item(
                "fungus_skewer",
                base_item="bread",
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
            ),
            Item(
                "honey_cookie",
                base_item="bread",
                food={"nutrition": 2, "saturation": 0.4},
            ),
            Item(
                "ice_cream_cone",
                base_item="bread",
                food={"nutrition": 2, "saturation": 0.4},
            ),
            Item(
                "ice_cream",
                base_item="bread",
                food={"nutrition": 4, "saturation": 3.6},
                max_stack_size=16,
            ),
            Item(
                "kelp_roll",
                base_item="bread",
                food={"nutrition": 10, "saturation": 12.6},
            ),
            Item(
                "kelp_roll_slice",
                base_item="bread",
                food={"nutrition": 2.5, "saturation": 6.2},
            ),
            Item(
                "melon_popsicle",
                base_item="bread",
                food={"nutrition": 3, "saturation": 0.5},
            ),
            Item(
                "mushroom_skewer",
                base_item="bread",
                food={"nutrition": 6, "saturation": 7.2},
                use_remainder={"id": "minecraft:stick"},
            ),
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
            ),
            Item(
                "potato_fries",
                base_item="bread",
                food={"nutrition": 1.5, "saturation": 1.5},
            ),
            Item(
                "salmon_roll",
                base_item="bread",
                food={"nutrition": 7, "saturation": 9.4},
            ),
            Item(
                "stuffed_potato",
                base_item="bread",
                food={"nutrition": 6, "saturation": 7.8},
            ),
            Item(
                "sweet_berry_cookie",
                base_item="bread",
                food={"nutrition": 2, "saturation": 0.4},
            ),
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
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="meals")

    def _create_recipes(self):
        """Create all meal recipes and add them to the bucket."""

        # Beef Skewer
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["b", "b", "s"],
                key={"b": "cooked_beef", "s": "stick"},
                result=self.bucket.get("beef_skewer"),
            ),
            category="meals",
        )

        # Beef Stew
        self.bucket.add_recipe(
            NewShapelessRecipe(
                ingredients=["bowl", "cooked_beef", "carrot", "baked_potato"],
                result=self.bucket.get("beef_stew"),
            ),
            category="meals",
        )

        # Fried Egg
        self.bucket.add_recipe(
            AutoCookingRecipe(
                ingredient="#minecraft:eggs",
                result=self.bucket.get("fried_egg"),
                base_cooking_time=140,
                experience=0.1,
            ),
            category="meals",
        )

        # Fruit Salad
        self.bucket.add_recipe(
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
            category="meals",
        )

        # Fungus Skewer (two variations)
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["w", "c", "s"],
                key={"w": "warped_fungus", "c": "crimson_fungus", "s": "stick"},
                result=self.bucket.get("fungus_skewer"),
            ),
            category="meals",
        )

        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["c", "w", "s"],
                key={"w": "warped_fungus", "c": "crimson_fungus", "s": "stick"},
                result=self.bucket.get("fungus_skewer"),
                recipe_id="fungus_skewer_reversed",
            ),
            category="meals",
        )

        # Honey Cookie
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["whw"],
                key={"h": "honey_bottle", "w": "wheat"},
                result=self.bucket.get("honey_cookie"),
            ),
            category="meals",
        )

        # Ice Cream Cone
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["W", "W", "W"],
                key={"W": "wheat"},
                result=self.bucket.get("ice_cream_cone"),
            ),
            category="meals",
        )

        # Ice Cream
        self.bucket.add_recipe(
            NewShapelessRecipe(
                ingredients=["snowball", "sugar", "bread"],
                result=self.bucket.get("ice_cream"),
            ),
            category="meals",
        )

        # Melon Popsicle
        self.bucket.add_recipe(
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
            category="meals",
        )

        # Mushroom Skewer (two variations)
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["b", "r", "s"],
                key={"b": "brown_mushroom", "r": "red_mushroom", "s": "stick"},
                result=self.bucket.get("mushroom_skewer"),
            ),
            category="meals",
        )

        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["r", "b", "s"],
                key={"b": "brown_mushroom", "r": "red_mushroom", "s": "stick"},
                result=self.bucket.get("mushroom_skewer"),
                recipe_id="mushroom_skewer_reversed",
            ),
            category="meals",
        )

        # Nether Salad
        self.bucket.add_recipe(
            NewShapelessRecipe(
                ingredients=["bowl", "crimson_fungus", "warped_fungus"],
                result=self.bucket.get("nether_salad"),
            ),
            category="meals",
        )

        # Potato Fries (cutting board)
        self.bucket.add_recipe(
            NewCuttingBoardRecipe(
                ingredient="baked_potato",
                result=self.bucket.get("potato_fries"),
                result_count=4,
            ),
            category="meals",
        )

        # Sweet Berry Cookie
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["wbw"],
                key={"b": "sweet_berries", "w": "wheat"},
                result=self.bucket.get("sweet_berry_cookie"),
            ),
            category="meals",
        )

        # Stuffed Potato
        self.bucket.add_recipe(
            NewShapelessRecipe(
                ingredients=["baked_potato", "cooked_beef", "carrot", "milk_bucket"],
                result=self.bucket.get("stuffed_potato"),
            ),
            category="meals",
        )

        # Warped Mutton
        self.bucket.add_recipe(
            NewShapelessRecipe(
                ingredients=["warped_roots", "warped_roots", "bowl", "cooked_mutton"],
                result=self.bucket.get("warped_mutton"),
            ),
            category="meals",
        )

        # Kelp Roll
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["rcr", "kkk"],
                key={
                    "k": "dried_kelp",
                    "r": self.bucket.get_ingredient("cooked_rice"),
                    "c": "carrot",
                },
                result=self.bucket.get("kelp_roll"),
            ),
            category="meals",
        )

        # Kelp Roll Slice (cutting board)
        self.bucket.add_recipe(
            NewCuttingBoardRecipe(
                ingredient=self.bucket.get("kelp_roll"),
                result=self.bucket.get("kelp_roll_slice"),
                result_count=4,
            ),
            category="meals",
        )

        # Salmon Roll
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["s", "s", "r"],
                key={
                    "s": self.bucket.get_ingredient("raw_salmon_slice"),
                    "r": self.bucket.get_ingredient("cooked_rice"),
                },
                result=self.bucket.get("salmon_roll"),
                result_count=2,
            ),
            category="meals",
        )

        # Cod Roll
        self.bucket.add_recipe(
            NewShapedRecipe(
                pattern=["c", "c", "r"],
                key={
                    "c": self.bucket.get_ingredient("raw_cod_slice"),
                    "r": self.bucket.get_ingredient("cooked_rice"),
                },
                result=self.bucket.get("cod_roll"),
                result_count=2,
            ),
            category="meals",
        )
