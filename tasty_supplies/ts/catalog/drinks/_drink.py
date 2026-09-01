from typing import List

from ts import Item, Shapeless, bases, stack


@stack(16)
class Drink(Item, abstract=True):
    """A potion in disguise, brewed in a crafting table.

    A horn version extends its bottled drink and swaps the container.
    """

    base = bases.POTION
    ingredients: List[str] = []
    container = "glass_bottle"

    def recipes(self) -> List:
        return [
            Shapeless(items=[*self.ingredients, self.container]),
            *super().recipes(),
        ]
