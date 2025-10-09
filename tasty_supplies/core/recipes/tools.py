from core.models import (
    TSContext,
    Item,
    ShapedRecipe,
    Result,
    Category,
    SmithingTransform,
)
from core.utils import to_absolute_path
from core import aliases


class Tools(Category):
    def __init__(self):
        super().__init__("Knife")

    def generate(self, ctx: TSContext):
        knife_pattern = ["m", "s"]

        def knife_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        def tool_attr(
            damage: float, speed: float, id_prefix: str, base_damage=1.0, base_speed=4.0
        ):
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
                                    "fallback": "Attack Damage",
                                },
                            ],
                        },
                    },
                },
            ]

        Item(
            "netherite_knife",
            SmithingTransform(
                base=aliases.DIAMOND_KNIFE,
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 2032,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(4.5, 2.3, "netherite_knife"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "diamond_knife",
            ShapedRecipe(
                key=knife_key("diamond"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 1561,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(4, 2.3, "diamond_knife"),
                    },
                ),
            ),
            base_item=aliases.DIAMOND_KNIFE,
        ).register(ctx)

        Item(
            "golden_knife",
            ShapedRecipe(
                key=knife_key("gold_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 32,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(2, 2.3, "golden_knife"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "iron_knife",
            ShapedRecipe(
                key=knife_key("iron_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 250,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(3.5, 2.3, "iron_knife"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "copper_knife",
            ShapedRecipe(
                key=knife_key("copper_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 190,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(3, 2.3, "copper_knife"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "flint_knife",
            ShapedRecipe(
                key=knife_key("flint"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 131,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(3, 2.3, "flint_knife"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        cleaver_pattern = ["mm", "mm", " s"]

        def cleaver_key(m: str):
            return {"m": to_absolute_path(m), "s": "minecraft:stick"}

        Item(
            "netherite_cleaver",
            SmithingTransform(
                base=aliases.DIAMOND_CLEAVER,
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 3046,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(9, 1.2, "netherite_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "diamond_cleaver",
            ShapedRecipe(
                key=cleaver_key("diamond"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 2341,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(8, 1.2, "diamond_cleaver"),
                    },
                ),
            ),
            base_item=aliases.DIAMOND_CLEAVER,
        ).register(ctx)

        Item(
            "golden_cleaver",
            ShapedRecipe(
                key=cleaver_key("gold_ingot"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 48,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(6, 1.2, "golden_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "iron_cleaver",
            ShapedRecipe(
                key=cleaver_key("iron_ingot"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 375,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(8, 1.1, "iron_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "copper_cleaver",
            ShapedRecipe(
                key=cleaver_key("copper_ingot"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 285,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(8, 1.0, "copper_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "stone_cleaver",
            ShapedRecipe(
                key=cleaver_key("#stone_crafting_materials"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 196,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(8, 1.0, "stone_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "wooden_cleaver",
            ShapedRecipe(
                key=cleaver_key("#planks"),
                pattern=cleaver_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 88,
                        "weapon": {},
                        "attribute_modifiers": tool_attr(6, 1.0, "wooden_cleaver"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)
