"""Tools category - contains all tool items and their recipes.

This module defines knives, cleavers, and other tools.
All items and recipes are managed through the Bucket system.
"""

from core.models import (
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
        super().__init__("Tools", bucket)

    def add_item(self, item, tool_type: str):
        if not item.components.get("custom_data"):
            item.components["custom_data"] = {}
        item.components["custom_data"]["ts_cutting_tool"] = tool_type
        return super().add_item(item)

    def create_items(self):
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

        self.add_item(
            Item(
                "netherite_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=2032,
                weapon={},
                attribute_modifiers=tool_attr(4.5, 2.3, "netherite_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "diamond_knife",
                base_item=aliases.DIAMOND_KNIFE,
                max_stack_size=1,
                max_damage=1561,
                weapon={},
                attribute_modifiers=tool_attr(4, 2.3, "diamond_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "golden_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=32,
                weapon={},
                attribute_modifiers=tool_attr(2, 2.3, "golden_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "iron_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=250,
                weapon={},
                attribute_modifiers=tool_attr(3.5, 2.3, "iron_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "copper_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=190,
                weapon={},
                attribute_modifiers=tool_attr(3, 2.3, "copper_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "flint_knife",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=131,
                weapon={},
                attribute_modifiers=tool_attr(3, 2.3, "flint_knife"),
            ),
            "knife",
        )

        self.add_item(
            Item(
                "netherite_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=3046,
                weapon={},
                attribute_modifiers=tool_attr(9, 1.2, "netherite_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "diamond_cleaver",
                base_item=aliases.DIAMOND_CLEAVER,
                max_stack_size=1,
                max_damage=2341,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.2, "diamond_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "golden_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=48,
                weapon={},
                attribute_modifiers=tool_attr(6, 1.2, "golden_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "iron_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=375,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.1, "iron_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "copper_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=285,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.0, "copper_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "stone_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=196,
                weapon={},
                attribute_modifiers=tool_attr(8, 1.0, "stone_cleaver"),
            ),
            "cleaver",
        )

        self.add_item(
            Item(
                "wooden_cleaver",
                base_item="wooden_sword",
                max_stack_size=1,
                max_damage=88,
                weapon={},
                attribute_modifiers=tool_attr(6, 1.0, "wooden_cleaver"),
            ),
            "cleaver",
        )

    def create_recipes(self):
        """Create all tool recipes and add them to the bucket."""
        knife_pattern = ["m", "s"]

        def knife_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        self.add_recipe(
            SmithingTransformRecipe(
                template="netherite_upgrade_smithing_template",
                base=self.bucket.get_ingredient("diamond_knife"),
                addition="netherite_ingot",
                result=self.bucket.get("netherite_knife"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=knife_key("diamond"),
                pattern=knife_pattern,
                result=self.bucket.get("diamond_knife"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=knife_key("gold_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("golden_knife"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=knife_key("iron_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("iron_knife"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=knife_key("copper_ingot"),
                pattern=knife_pattern,
                result=self.bucket.get("copper_knife"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=knife_key("flint"),
                pattern=knife_pattern,
                result=self.bucket.get("flint_knife"),
            )
        )
        cleaver_pattern = ["mm", "mm", " s"]

        def cleaver_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        self.add_recipe(
            SmithingTransformRecipe(
                template="netherite_upgrade_smithing_template",
                base=self.bucket.get_ingredient("diamond_cleaver"),
                addition="netherite_ingot",
                result=self.bucket.get("netherite_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("diamond"),
                pattern=cleaver_pattern,
                result=self.bucket.get("diamond_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("gold_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("golden_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("iron_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("iron_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("copper_ingot"),
                pattern=cleaver_pattern,
                result=self.bucket.get("copper_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("#stone_crafting_materials"),
                pattern=cleaver_pattern,
                result=self.bucket.get("stone_cleaver"),
            )
        )

        self.add_recipe(
            ShapedRecipe(
                key=cleaver_key("#planks"),
                pattern=cleaver_pattern,
                result=self.bucket.get("wooden_cleaver"),
            )
        )
