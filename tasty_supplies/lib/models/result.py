from typing import List

from .tools import to_absolute_path


class Effect:
    def __init__(self, effect: str, duration: int = 0, amplifier: int = 0):
        self.effect = effect
        self.duration = duration
        self.amplifier = amplifier

    def _to_json(self) -> dict:
        return {
            "id": to_absolute_path(self.effect),
            "duration": self.duration,
            "amplifier": self.amplifier,
        }


class Result:
    def __init__(
        self, count: int = 1, max_stack_size: int = 64, extra_components: dict = {}
    ):
        self.count = count
        self.max_stack_size = max_stack_size
        self.components = extra_components

    def _to_json(self, item_name: str, base_item: str) -> dict:
        return {
            "id": f"minecraft:{base_item}",
            "components": self._get_components_json(item_name),
            "max_stack_size": self.max_stack_size,
            "count": self.count,
        }

    def _get_components_json(self, item_name: str) -> dict:
        return (
            self.components
            | {
                "custom_name": {
                    "text": item_name.replace("_", " ").title(),
                    "italic": False,
                },
                "custom_model_data": {"strings": [f"tasty_supplies/{item_name}"]},
            }
            | self.components
        )


class FoodResult(Result):
    def __init__(
        self,
        count: int = 1,
        max_stack_size: int = 64,
        nutrition: int = 0,
        saturation: float = 0.0,
        can_always_eat: bool = False,
        effects: List[Effect] = [],
        extra_components: dict = {},
    ):
        extra_components["food"] = {
            "nutrition": nutrition,
            "saturation": saturation,
            "can_always_eat": can_always_eat,
        }

        extra_components["consumable"] = {
            "on_consume_effects": [
                {
                    "type": "apply_effects",
                    "effects": [effect._to_json() for effect in effects],
                }
            ],
        }

        super().__init__(count, max_stack_size, extra_components)


class PotionResult(Result):
    def __init__(
        self,
        count: int = 1,
        max_stack_size: int = 1,
        extra_components: dict = {},
        potion_effects: List[Effect] = [],
    ):
        extra_components["potion_contents"] = {
            "potion_contents": {
                "custom_color": 16777215,
                "custom_effects": [effect._to_json() for effect in potion_effects],
            }
        }

        super().__init__(count, max_stack_size, extra_components)
