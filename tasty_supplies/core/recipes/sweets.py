"""Sweets category - contains all dessert items and their recipes.

This module defines sweet foods including pies, cakes, cookies, and other desserts.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    TSContext,
    Bucket,
    Item,
    ShapelessRecipe,
    ShapedRecipe,
    CuttingBoardRecipe,
    AutoCookingRecipe,
    Category,
    aliases,
)


class Sweets(Category):
    """Category for sweet dessert items."""

    def __init__(self, bucket: Bucket):
        """Initialize Sweets category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Sweets", bucket)

    def generate(self, ctx: TSContext):
        """Generate all sweet items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all sweet items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all sweet recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all sweet items and add them to the bucket."""
        items = [
            # Butter and clear effects
            Item(
                "butter",
                base_item=aliases.BUTTER,
                food={"nutrition": 2, "saturation": 1.2},
                consumable={"on_consume_effects": [{"type": "clear_all_effects"}]},
            ),
            # Pie Crust
            Item("pie_crust", base_item=aliases.PIE_CRUST),
            # Apple Pie
            Item(
                "apple_pie", base_item="bread", food={"nutrition": 8, "saturation": 6}
            ),
            Item(
                "apple_pie_slice",
                base_item="bread",
                food={"nutrition": 2, "saturation": 1.5},
            ),
            # Cheese
            Item("cheese", base_item="bread", food={"nutrition": 8, "saturation": 5.6}),
            Item(
                "cheese_slice",
                base_item="bread",
                food={"nutrition": 2, "saturation": 1.4},
            ),
            # Cherry Blossom Pie
            Item(
                "cherry_blossom_pie",
                base_item="bread",
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
            ),
            Item(
                "cherry_blossom_pie_slice",
                base_item="bread",
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
            ),
            # Chocolate Pie
            Item(
                "chocolate_pie",
                base_item="bread",
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
            ),
            Item(
                "chocolate_pie_slice",
                base_item="bread",
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
            ),
            # Chorus Pie
            Item(
                "chorus_pie",
                base_item="bread",
                food={"nutrition": 8, "saturation": 6},
                consumable={
                    "on_consume_effects": [
                        {"type": "teleport_randomly", "diameter": 32}
                    ]
                },
                use_cooldown={"seconds": 2.0, "cooldown_group": "chorus_pie"},
            ),
            Item(
                "chorus_pie_slice",
                base_item="bread",
                food={"nutrition": 2, "saturation": 1.5},
                consumable={
                    "on_consume_effects": [{"type": "teleport_randomly", "diameter": 8}]
                },
                use_cooldown={"seconds": 1.0, "cooldown_group": "chorus_pie"},
            ),
            # Glow Berry Pie
            Item(
                "glow_berry_pie",
                base_item="bread",
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
            ),
            Item(
                "glow_berry_pie_slice",
                base_item="bread",
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
            ),
            # Sweet Berry Cheesecake
            Item(
                "sweet_berry_cheesecake",
                base_item="bread",
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
            ),
            Item(
                "sweet_berry_cheesecake_slice",
                base_item="bread",
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
            ),
            # Croissant
            Item(
                "croissant", base_item="bread", food={"nutrition": 6, "saturation": 3.4}
            ),
            # Honeyed Apple
            Item(
                "honeyed_apple",
                base_item="bread",
                food={"nutrition": 6, "saturation": 8.6},
            ),
            # Sweet Roll
            Item(
                "sweet_roll",
                base_item="bread",
                food={"nutrition": 8, "saturation": 12.8},
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="sweets")

    def _create_recipes(self):
        """Create all sweet recipes and add them to the bucket."""

        # Butter
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=["milk_bucket"],
                result=self.bucket.get("butter"),
            ),
            category="sweets",
        )

        # Pie Crust
        self.bucket.add_recipe(
            ShapedRecipe(
                pattern=["WBW", " W "],
                key={"W": "wheat", "B": self.bucket.get_ingredient("butter")},
                result=self.bucket.get("pie_crust"),
            ),
            category="sweets",
        )

        # Apple Pie
        self.bucket.add_recipe(
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
            category="sweets",
        )

        # Apple Pie Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("apple_pie"),
                result=self.bucket.get("apple_pie_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Cheese
        self.bucket.add_recipe(
            AutoCookingRecipe(
                ingredient="milk_bucket",
                result=self.bucket.get("cheese"),
                base_cooking_time=200,
                experience=0.5,
            ),
            category="sweets",
        )

        # Cheese Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("cheese"),
                result=self.bucket.get("cheese_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Cherry Blossom Pie
        self.bucket.add_recipe(
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
            category="sweets",
        )

        # Cherry Blossom Pie Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("cherry_blossom_pie"),
                result=self.bucket.get("cherry_blossom_pie_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Chocolate Pie
        self.bucket.add_recipe(
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
            category="sweets",
        )

        # Chocolate Pie Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("chocolate_pie"),
                result=self.bucket.get("chocolate_pie_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Chorus Pie
        self.bucket.add_recipe(
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
            category="sweets",
        )

        # Chorus Pie Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("chorus_pie"),
                result=self.bucket.get("chorus_pie_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Glow Berry Pie
        self.bucket.add_recipe(
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
            category="sweets",
        )

        # Glow Berry Pie Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("glow_berry_pie"),
                result=self.bucket.get("glow_berry_pie_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Sweet Berry Cheesecake
        self.bucket.add_recipe(
            ShapedRecipe(
                pattern=["SSS", "SSS", "MBM"],
                key={
                    "S": "sweet_berries",
                    "M": "milk_bucket",
                    "B": self.bucket.get_ingredient("pie_crust"),
                },
                result=self.bucket.get("sweet_berry_cheesecake"),
            ),
            category="sweets",
        )

        # Sweet Berry Cheesecake Slice
        self.bucket.add_recipe(
            CuttingBoardRecipe(
                ingredient=self.bucket.get("sweet_berry_cheesecake"),
                result=self.bucket.get("sweet_berry_cheesecake_slice"),
                result_count=4,
            ),
            category="sweets",
        )

        # Croissant
        self.bucket.add_recipe(
            ShapedRecipe(
                pattern=["WBS", "WBS"],
                key={
                    "W": "wheat",
                    "B": self.bucket.get_ingredient("butter"),
                    "S": "sugar",
                },
                result=self.bucket.get("croissant"),
            ),
            category="sweets",
        )

        # Honeyed Apple
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "honey_bottle"],
                result=self.bucket.get("honeyed_apple"),
            ),
            category="sweets",
        )

        # Sweet Roll
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "wheat",
                    "sugar",
                    "#minecraft:eggs",
                    self.bucket.get_ingredient("butter"),
                ],
                result=self.bucket.get("sweet_roll"),
            ),
            category="sweets",
        )
