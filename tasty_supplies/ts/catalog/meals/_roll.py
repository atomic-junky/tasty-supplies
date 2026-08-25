from typing import List

from ts import Item, Shaped

from ..ingredients.rice import CookedRice


class Roll(Item, abstract=True):
    filling: type

    def recipes(self) -> List:
        return [
            Shaped(
                pattern=["f", "f", "r"],
                key={"f": self.filling, "r": CookedRice},
                count=2,
            ),
            *super().recipes(),
        ]
