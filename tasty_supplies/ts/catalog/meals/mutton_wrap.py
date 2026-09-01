from ts import Item, food, shapeless

from ..ingredients.rice import CookedRice


@food(14, 24.4)
@shapeless("bread", "cooked_mutton", CookedRice, "kelp")
class MuttonWrap(Item):
    pass
