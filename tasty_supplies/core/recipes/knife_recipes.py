from .. import TSContext, Item, ShapedRecipe, Result, Category


class KnifeCategory(Category):
    def __init__(self):
        super().__init__("Knife")

    def generate(self, ctx: TSContext):
        knife_pattern = ["m", "s"]

        def knife_shape(m: str):
            return {"m": f"minecraft:{m}", "s": "minecraft:stick"}

        def knife_attr(damage: float, speed: float, id_prefix: str):
            base_damage = 4
            base_speed = 1.6

            return [
                {
                    "type": "attack_damage",
                    "slot": "mainhand",
                    "id": f"tasty_supplies:{id_prefix}_knife_damage",
                    "amount": max(round(damage - base_damage, 1), 0),
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
                    "id": f"tasty_supplies:{id_prefix}_knife_speed",
                    "amount": max(round(speed - base_speed, 1), 0),
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
            ShapedRecipe(
                key=knife_shape("netherite_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 2032,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(4.5, 2.3, "netherite"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "diamond_knife",
            ShapedRecipe(
                key=knife_shape("diamond"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 1561,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(4, 2.3, "diamond"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "golden_knife",
            ShapedRecipe(
                key=knife_shape("gold_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 32,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(2, 2.3, "golden"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "iron_knife",
            ShapedRecipe(
                key=knife_shape("iron_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 250,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(3.5, 2.3, "iron"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "copper_knife",
            ShapedRecipe(
                key=knife_shape("copper_ingot"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 190,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(3, 2.3, "copper"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)

        Item(
            "flint_knife",
            ShapedRecipe(
                key=knife_shape("flint"),
                pattern=knife_pattern,
                category="equipement",
                result=Result(
                    max_stack_size=1,
                    extra_components={
                        "max_damage": 131,
                        "weapon": {},
                        "attribute_modifiers": knife_attr(3, 2.3, "flint"),
                    },
                ),
            ),
            base_item="wooden_sword",
        ).register(ctx)
