from typing import Any, Dict

from ts import Item, bases


class Equippable(Item, abstract=True):
    base = bases.LEATHER_HELMET
    slot = "head"

    @classmethod
    def declaration(cls):
        declaration = super().declaration()
        declaration.components["equippable"] = {
            "slot": cls.slot,
            "dispensable": True,
            "swappable": True,
        }
        return declaration

    @property
    def model_case(self) -> Dict[str, Any]:
        """Selects the worn model on the head, the flat one everywhere else."""

        return {
            "when": f"tasty_supplies/{self.id}",
            "model": {
                "type": "minecraft:select",
                "property": "minecraft:display_context",
                "cases": [
                    {
                        "when": self.slot,
                        "model": {
                            "type": "minecraft:model",
                            "model": f"tasty_supplies:item/equipement/{self.id}",
                        },
                    }
                ],
                "fallback": {
                    "type": "minecraft:model",
                    "model": self.model_path,
                },
            },
        }
