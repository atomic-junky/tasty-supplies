"""Beverage category - contains all drink items and their recipes.

This module defines beverages including ciders, custards, juices, and special drinks.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    TSContext,
    Bucket,
    Item,
    ShapelessRecipe,
    Category,
)


class Beverage(Category):
    """Category for beverage items."""

    def __init__(self, bucket: Bucket):
        """Initialize Beverage category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Drinks", bucket)

    def generate(self, ctx: TSContext):
        """Generate all beverage items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all beverage items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all beverage recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all beverage items and add them to the bucket."""
        items = [
            # Apple Cider
            Item(
                "apple_cider",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:absorption",
                            "duration": 1800,
                            "amplifier": 1,
                        }
                    ]
                },
            ),
            Item(
                "apple_cider_horn",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:absorption",
                            "duration": 1800,
                            "amplifier": 1,
                        }
                    ]
                },
                use_remainder={"id": "minecraft:goat_horn"},
            ),
            # Glow Berry Custard
            Item(
                "glow_berry_custard",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:glowing",
                            "duration": 3600,
                            "amplifier": 0,
                        }
                    ]
                },
            ),
            Item(
                "glow_berry_custard_horn",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:glowing",
                            "duration": 3600,
                            "amplifier": 0,
                        }
                    ]
                },
                use_remainder={"id": "minecraft:goat_horn"},
            ),
            # Hot Cocoa
            Item(
                "hot_cocoa",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:regeneration",
                            "duration": 600,
                            "amplifier": 0,
                        }
                    ]
                },
            ),
            Item(
                "hot_cocoa_horn",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:regeneration",
                            "duration": 600,
                            "amplifier": 0,
                        }
                    ]
                },
                use_remainder={"id": "minecraft:goat_horn"},
            ),
            # Melon Juice
            Item(
                "melon_juice",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {"id": "minecraft:instant_health", "amplifier": 0}
                    ]
                },
            ),
            Item(
                "melon_juice_horn",
                base_item="potion",
                max_stack_size=1,
                potion_contents={
                    "custom_effects": [
                        {"id": "minecraft:instant_health", "amplifier": 0}
                    ]
                },
                use_remainder={"id": "minecraft:goat_horn"},
            ),
            # Magma Gelatin (food item, not potion)
            Item(
                "magma_gelatin",
                base_item="bread",
                food={"nutrition": 1, "saturation": 6, "can_always_eat": True},
                max_stack_size=1,
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:nausea",
                                    "duration": 300,
                                    "amplifier": 0,
                                },
                                {
                                    "id": "minecraft:fire_resistance",
                                    "duration": 6000,
                                    "amplifier": 0,
                                },
                            ],
                        }
                    ]
                },
                use_remainder={"id": "minecraft:bucket"},
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="beverages")

    def _create_recipes(self):
        """Create all beverage recipes and add them to the bucket."""

        # Apple Cider
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "glass_bottle"],
                result=self.bucket.get("apple_cider"),
            ),
            category="beverages",
        )

        # Apple Cider Horn
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "goat_horn"],
                result=self.bucket.get("apple_cider_horn"),
            ),
            category="beverages",
        )

        # Glow Berry Custard
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "glow_berries",
                    "milk_bucket",
                    "egg",
                    "sugar",
                    "glass_bottle",
                ],
                result=self.bucket.get("glow_berry_custard"),
            ),
            category="beverages",
        )

        # Glow Berry Custard Horn
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "glow_berries",
                    "milk_bucket",
                    "egg",
                    "sugar",
                    "goat_horn",
                ],
                result=self.bucket.get("glow_berry_custard_horn"),
            ),
            category="beverages",
        )

        # Hot Cocoa
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "cocoa_beans",
                    "cocoa_beans",
                    "milk_bucket",
                    "sugar",
                    "glass_bottle",
                ],
                result=self.bucket.get("hot_cocoa"),
            ),
            category="beverages",
        )

        # Hot Cocoa Horn
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "cocoa_beans",
                    "cocoa_beans",
                    "milk_bucket",
                    "sugar",
                    "goat_horn",
                ],
                result=self.bucket.get("hot_cocoa_horn"),
            ),
            category="beverages",
        )

        # Melon Juice
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "sugar",
                    "glass_bottle",
                ],
                result=self.bucket.get("melon_juice"),
            ),
            category="beverages",
        )

        # Melon Juice Horn
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "melon_slice",
                    "sugar",
                    "goat_horn",
                ],
                result=self.bucket.get("melon_juice_horn"),
            ),
            category="beverages",
        )

        # Magma Gelatin (food item, not potion)
        self.bucket.add_recipe(
            ShapelessRecipe(
                ingredients=[
                    "bucket",
                    "magma_cream",
                    "magma_cream",
                    "magma_cream",
                    "blaze_powder",
                    "blaze_powder",
                ],
                result=self.bucket.get("magma_gelatin"),
            ),
            category="beverages",
        )
