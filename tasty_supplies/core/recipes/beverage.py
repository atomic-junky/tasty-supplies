"""Beverage category - contains all drink items and their recipes.

This module defines beverages including ciders, custards, juices, and special drinks.
All items and recipes are managed through the Bucket system.
"""

from .. import (
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

    def create_items(self):
        """Create all beverage items and add them to the bucket."""
        self.add_item(
            Item(
                "apple_cider",
                base_item="potion",
                max_stack_size=16,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:absorption",
                            "duration": 1800,
                            "amplifier": 1,
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "apple_cider_horn",
                base_item="potion",
                max_stack_size=16,
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
            )
        )

        self.add_item(
            Item(
                "glow_berry_custard",
                base_item="potion",
                max_stack_size=16,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:glowing",
                            "duration": 3600,
                            "amplifier": 0,
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "glow_berry_custard_horn",
                base_item="potion",
                max_stack_size=16,
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
            )
        )

        self.add_item(
            Item(
                "hot_cocoa",
                base_item="potion",
                max_stack_size=16,
                potion_contents={
                    "custom_effects": [
                        {
                            "id": "minecraft:regeneration",
                            "duration": 600,
                            "amplifier": 0,
                        }
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "hot_cocoa_horn",
                base_item="potion",
                max_stack_size=16,
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
            )
        )

        self.add_item(
            Item(
                "melon_juice",
                base_item="potion",
                max_stack_size=16,
                potion_contents={
                    "custom_effects": [
                        {"id": "minecraft:instant_health", "amplifier": 0}
                    ]
                },
            )
        )

        self.add_item(
            Item(
                "melon_juice_horn",
                base_item="potion",
                max_stack_size=16,
                potion_contents={
                    "custom_effects": [
                        {"id": "minecraft:instant_health", "amplifier": 0}
                    ]
                },
                use_remainder={"id": "minecraft:goat_horn"},
            )
        )

        self.add_item(
            Item(
                "magma_gelatin",
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
            )
        )

    def create_recipes(self):
        """Create all beverage recipes and add them to the bucket."""

        self.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "glass_bottle"],
                result=self.bucket.get("apple_cider"),
            ),
        )

        self.add_recipe(
            ShapelessRecipe(
                ingredients=["apple", "apple", "sugar", "goat_horn"],
                result=self.bucket.get("apple_cider_horn"),
            ),
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )

        self.add_recipe(
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
        )
