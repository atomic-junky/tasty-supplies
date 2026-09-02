from typing import List

from ts import Brewing, Item, Shapeless, bases, stack, disable
from ts.catalog.tools.tankard import Tankard
from ts.recipe import Ref
from ts.utils import title_case


@stack(16)
class Potion(Item, abstract=True):
    pass


class Drink(Potion, abstract=True):
    base = bases.POTION
    ingredients: List[str] = []
    container = "glass_bottle"

    def recipes(self) -> List:
        return [
            Shapeless(items=[*self.ingredients, self.container]),
            *super().recipes(),
        ]


class AlcoholDrink(Potion, abstract=True):
    base = bases.POTION
    container = Tankard
    reagent: Ref

    def recipes(self) -> List:
        return [
            Brewing(input=self.container, reagent=self.reagent),
            *super().recipes(),
        ]
