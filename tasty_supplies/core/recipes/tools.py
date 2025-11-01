"""Tools category - contains all tool items and their recipes.

This module defines knives, cleavers, and other tools.
All items and recipes are managed through the Bucket system.
"""

from core.models import (
    TSContext,
    Item,
    ShapedRecipe,
    SmithingTransformRecipe,
    Category,
)
from core.bucket import Bucket
from core.utils import to_absolute_path
from core import aliases


class Tools(Category):
    """Category for tool items."""

    def __init__(self, bucket: Bucket):
        """Initialize Tools category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Knife", bucket)

    def generate(self, ctx: TSContext):
        """Generate all tool items and recipes.

        Args:
            ctx: The Tasty Supplies context
        """
        pass  # Items and recipes are now created in separate phases

    def create_items(self):
        """Phase 1: Create all tool items."""
        self._create_items()

    def create_recipes(self):
        """Phase 2: Create all tool recipes."""
        self._create_recipes()

    def _create_items(self):
        """Create all tool items and add them to the bucket."""

        def tool_attr(
            damage: float, speed: float, id_prefix: str, base_damage=1.0, base_speed=4.0
        ):
            """Helper to generate tool attribute modifiers."""
            return [
                {
                    "type": "attack_damage",
                    "slot": "mainhand",
                    "id": f"tasty_supplies:{id_prefix}_damage",
                    "amount": round(damage - base_damage, 1),
                    "operation": "add_value",
                    "display": {
                        "type": "override",
                        "value": {
                            "type": "translatable",
                            "translate": "attribute.modifier.equals.0",
                            "fallback": "%s %s",
                            "color": "dark_green",
                            "with": [
                                {"text": f" {str(damage)}"},
                                {
                                    "type": "translatable",
                                    "translate": "attribute.name.attack_damage",
                                    "fallback": "Attack Damage",
                                },
                            ],
                        },
                    },
                },
                {
                    "type": "attack_speed",
                    "slot": "mainhand",
                    "id": f"tasty_supplies:{id_prefix}_speed",
                    "amount": round(speed - base_speed, 1),
                    "operation": "add_value",
                    "display": {
                        "type": "override",
                        "value": {
                            "type": "translatable",
                            "translate": "attribute.modifier.equals.0",
                            "fallback": "%s %s",
                            "color": "dark_green",
                            "with": [
                                {"text": f" {str(speed)}"},
                                {
                                    "type": "translatable",
                                    "translate": "attribute.name.attack_speed",
                                    "fallback": "Attack Speed",
                                },
                            ],
                        },
                    },
                },
            ]

        items = [
            # Knives - All properties defined here
            Item(
                "netherite_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=2032,
                weapon={},
                attribute_modifiers=tool_attr(4.5, 2.3, "netherite_knife"),
            ),
            Item(
                "diamond_knife",
                base_item=aliases.DIAMOND_KNIFE,
                max_stack_size=1,
                max_damage=1561,
                weapon={},
                attribute_modifiers=tool_attr(4, 2.3, "diamond_knife"),
            ),
            Item(
                "golden_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=32,
                weapon={},
                attribute_modifiers=tool_attr(2, 2.3, "golden_knife"),
            ),
            Item(
                "iron_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=250,
                weapon={},
                attribute_modifiers=tool_attr(3.5, 2.3, "iron_knife"),
            ),
            Item(
                "copper_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=190,
                weapon={},
                attribute_modifiers=tool_attr(3, 2.3, "copper_knife"),
            ),
            Item(
                "flint_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=131,
                weapon={},
                attribute_modifiers=tool_attr(3, 2.3, "flint_knife"),
            ),
            # Cleavers - All properties defined here
            Item(
                "netherite_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=3046,
                weapon={},
                attribute_modifiers=tool_attr(9, 1.2, "netherite_cleaver"),
            ),
            Item(
                "diamond_cleaver",
                base_item=aliases.DIAMOND_CLEAVER,
                max_stack_size=1,
                max_damage=2341,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.2, "diamond_cleaver"),
            ),
            Item(
                "golden_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=48,
                weapon={},
                attribute_modifiers=tool_attr(6, 1.2, "golden_cleaver"),
            ),
            Item(
                "iron_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=375,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.1, "iron_cleaver"),
            ),
            Item(
                "copper_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=285,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.0, "copper_cleaver"),
            ),
            Item(
                "stone_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=196,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.0, "stone_cleaver"),
            ),
            Item(
                "wooden_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=88,
                weapon={},
                attribute_modifiers=tool_attr(6, 1.0, "wooden_cleaver"),
            ),
        ]

        for item in items:
            self.bucket.add_item(item, category="tools")

    def _create_recipes(self):
        """Create all tool recipes and add them to the bucket."""
        knife_pattern = ["m", "s"]

        def knife_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        # Knife recipes, no item properties
        self.bucket.add_recipe(
            SmithingTransformRecipe(
                template="netherite_upgrade_smithing_template",
                base=self.bucket.get_ingredient("diamond_knife"),
                addition="netherite_ingot",
                result=self.bucket.get("netherite_knife"),
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=knife_key("diamond"),
                pattern=knife_pattern,
                result=self.bucket.get("diamond_knife"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=knife_key("gold_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("golden_knife"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=knife_key("iron_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("iron_knife"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=knife_key("copper_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("copper_knife"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=knife_key("flint"),
                pattern=knife_pattern,
                result=self.bucket.get("flint_knife"),
                category="equipment",
            )
        )

        # Cleaver recipes
        cleaver_pattern = ["mm", "mm", " s"]

        def cleaver_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        self.bucket.add_recipe(
            SmithingTransformRecipe(
                template="netherite_upgrade_smithing_template",
                base=self.bucket.get_ingredient("diamond_cleaver"),
                addition="netherite_ingot",
                result=self.bucket.get("netherite_cleaver"),
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("diamond"),
                pattern=cleaver_pattern,
                result=self.bucket.get("diamond_cleaver"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("gold_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("golden_cleaver"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("iron_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("iron_cleaver"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("copper_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("copper_cleaver"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("#stone_crafting_materials"),
                pattern=cleaver_pattern,
                result=self.bucket.get("stone_cleaver"),
                category="equipment",
            )
        )

        self.bucket.add_recipe(
            ShapedRecipe(
                key=cleaver_key("#planks"),
                pattern=cleaver_pattern,
                result=self.bucket.get("wooden_cleaver"),
                category="equipment",
            )
        )
