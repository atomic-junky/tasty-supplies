from typing import List

from ts import Cut, Item, Shaped, food

from ..ingredients.pie_crust import PieCrust


@food(8, 6)
class Pie(Item, abstract=True):
    top: str
    middle: str
    sides: str

    def recipes(self) -> List:
        return [
            Shaped(
                pattern=["TTT", "MMM", "SCS"],
                key={
                    "T": self.top,
                    "M": self.middle,
                    "S": self.sides,
                    "C": PieCrust,
                },
            ),
            *super().recipes(),
        ]


@food(2, 1.5)
class PieSlice(Item, abstract=True):
    source: type
    slices: int = 4

    def recipes(self) -> List:
        return [Cut(count=self.slices, ingredient=self.source), *super().recipes()]
