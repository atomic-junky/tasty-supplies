"""Sweets category - contains all dessert items and their recipes.

This module defines sweet foods including pies, cakes, cookies, and other desserts.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    Bucket,
    Item,
    ShapelessRecipe,
    ShapedRecipe,
    CuttingBoardRecipe,
    Category,
)


class Sweets(Category):
    """Category for sweet dessert items."""

    def __init__(self, bucket: Bucket):
        """Initialize Sweets category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Sweets", bucket)

    def create_items(self):
        """Create all sweet items and add them to the bucket."""

        self.add_item(Item("apple_pie", food={"nutrition": 8, "saturation": 6}))

        self.add_item(
            Item(
                "apple_pie_slice",
                food={"nutrition": 2, "saturation": 1.5},
            )
        )

        self.add_item(
            Item(
                "cherry_blossom_pie",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:slow_falling",
                                    "duration": 3600,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "cherry_blossom_pie_slice",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:slow_falling",
                                    "duration": 900,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "chocolate_pie",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:speed",
                                    "duration": 3600,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "chocolate_pie_slice",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:speed",
                                    "duration": 900,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "chorus_pie",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {"type": "teleport_randomly", "diameter": 32}
                    ]
                },
                use_cooldown={"seconds": 2.0, "cooldown_group": "chorus_pie"},
            )
        )

        self.add_item(
            Item(
                "chorus_pie_slice",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [{"type": "teleport_randomly", "diameter": 8}]
                },
                use_cooldown={"seconds": 1.0, "cooldown_group": "chorus_pie"},
            )
        )

        self.add_item(
            Item(
                "glow_berry_pie",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:glowing",
                                    "duration": 3600,
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
                "glow_berry_pie_slice",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:glowing",
                                    "duration": 900,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
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
                "melon_popsicle",
                food={"nutrition": 3, "saturation": 0.5},
            )
        )

        self.add_item(
            Item(
                "sweet_berry_cheesecake",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:speed",
                                    "duration": 3600,
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
                "sweet_berry_cheesecake_slice",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:speed",
                                    "duration": 900,
                                    "amplifier": 1,
                                }
                            ],
                        }
                    ]
                },
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
                "sweet_berry_cookie",
                food={"nutrition": 2, "saturation": 0.4},
            )
        )

        self.add_item(Item("croissant", food={"nutrition": 6, "saturation": 3.4}))

        self.add_item(
            Item(
                "honeyed_apple",
                food={"nutrition": 6, "saturation": 8.6},
            )
        )

        self.add_item(
            Item(
                "sweet_roll",
                food={"nutrition": 8, "saturation": 12.8},
            )
        )

    def create_recipes(self):
        """Create all sweet recipes and add them to the bucket."""

        self.add_recipe(
            ShapelessRecipe(
                ingredients=["milk_bucket"],
                result=self.bucket.get("butter"),
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["WBW", " W "],
                key={"W": "wheat", "B": self.bucket.get_ingredient("butter")},
                result=self.bucket.get("pie_crust"),
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["WWW", "AAA", "SBS"],
                key={
                    "W": "wheat",
                    "A": "apple",
                    "S": "sugar",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("apple_pie"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("apple_pie"),
                result=self.bucket.get("apple_pie_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["CCC", "MMM", "HBH"],
                key={
                    "C": "cherry_leaves",
                    "M": "milk_bucket",
                    "H": "honeycomb",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("cherry_blossom_pie"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("cherry_blossom_pie"),
                result=self.bucket.get("cherry_blossom_pie_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["CCC", "MMM", "SBS"],
                key={
                    "C": "cocoa_beans",
                    "M": "milk_bucket",
                    "S": "sugar",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("chocolate_pie"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("chocolate_pie"),
                result=self.bucket.get("chocolate_pie_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["CCC", "SSS", "MPM"],
                key={
                    "C": "chorus_fruit",
                    "M": "milk_bucket",
                    "S": "sugar",
                    "P": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("chorus_pie"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("chorus_pie"),
                result=self.bucket.get("chorus_pie_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "snowball",
                    "sugar",
                    self.bucket.get_ingredient("ice_cream_cone"),
                ],
                result=self.bucket.get("ice_cream"),
            ),
        )

        self.add_recipe(
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
                result=self.bucket.get("melon_popsicle"),
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["GGG", "SSS", "MBM"],
                key={
                    "G": "glow_berries",
                    "M": "milk_bucket",
                    "S": "sugar",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("glow_berry_pie"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("glow_berry_pie"),
                result=self.bucket.get("glow_berry_pie_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["SSS", "SSS", "MBM"],
                key={
                    "S": "sweet_berries",
                    "M": "milk_bucket",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("sweet_berry_cheesecake"),
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("sweet_berry_cheesecake"),
                result=self.bucket.get("sweet_berry_cheesecake_slice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["whw"],
                key={"h": "honey_bottle", "w": "wheat"},
                result=self.bucket.get("honey_cookie"),
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["wbw"],
                key={"b": "sweet_berries", "w": "wheat"},
                result=self.bucket.get("sweet_berry_cookie"),
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                pattern=["WBS", "WBS"],
                key={
                    "W": "wheat",
                    "B": self.bucket.get_ingredient("butter"),
                    "S": "sugar",
                },
                result=self.bucket.get("croissant"),
            ),
        )

        self.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "honey_bottle"],
                result=self.bucket.get("honeyed_apple"),
            ),
        )

        self.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "wheat",
                    "sugar",
                    "#minecraft:eggs",
                    self.bucket.get_ingredient("butter"),
                ],
                result=self.bucket.get("sweet_roll"),
            ),
        )
