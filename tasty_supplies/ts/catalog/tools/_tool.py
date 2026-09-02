"""Knives and cleavers.

A tool states its material, damage, attack speed and durability; the model,
the attribute modifiers and the cutting tag follow from those.
"""

from typing import Any, Dict, List

from ts import Item, Shaped, bases, component, stack


def _modifier(
    tool_id: str, attribute: str, label: str, value: float, base: float
) -> Dict[str, Any]:
    """An attribute modifier, displayed as the value it adds up to."""

    return {
        "type": attribute,
        "slot": "mainhand",
        "id": f"tasty_supplies:{tool_id}_{attribute.removeprefix('attack_')}",
        "amount": round(value - base, 1),
        "operation": "add_value",
        "display": {
            "type": "override",
            "value": {
                "type": "translatable",
                "translate": "attribute.modifier.equals.0",
                "fallback": "%s %s",
                "color": "dark_green",
                "with": [
                    {"text": f" {value}"},
                    {
                        "type": "translatable",
                        "translate": f"attribute.name.{attribute}",
                        "fallback": label,
                    },
                ],
            },
        },
    }


@stack(1)
@component(weapon={})
class Tool(Item, abstract=True):
    base = bases.WOODEN_SWORD
    parent_model = "minecraft:item/handheld"

    #: Read by the cutting board, which only accepts a knife or a cleaver.
    kind: str
    material: Any = None
    damage: float = 1.0
    speed: float = 4.0
    durability: int = 1
    pattern: List[str] = []

    @classmethod
    def declaration(cls):
        declaration = super().declaration()
        declaration.components.update(
            {
                "max_damage": cls.durability,
                "attribute_modifiers": [
                    _modifier(
                        cls.id, "attack_damage", "Attack Damage", cls.damage, 1.0
                    ),
                    _modifier(cls.id, "attack_speed", "Attack Speed", cls.speed, 4.0),
                ],
                "custom_data": {
                    **declaration.components.get("custom_data", {}),
                    "ts_cutting_tool": cls.kind,
                },
            }
        )
        return declaration

    def recipes(self) -> List:
        specs = super().recipes()
        if self.material:
            specs.insert(
                0,
                Shaped(pattern=self.pattern, key={"m": self.material, "s": "stick"}),
            )
        return specs


class Knife(Tool, abstract=True):
    kind = "knife"
    pattern = ["m", "s"]
    speed = 2.3


class Cleaver(Tool, abstract=True):
    kind = "cleaver"
    pattern = ["mm", "mm", " s"]
