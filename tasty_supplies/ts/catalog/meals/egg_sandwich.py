from ts import Item, food, shapeless

from .fried_egg import FriedEgg


@food(11, 16.4)
@shapeless("bread", FriedEgg, FriedEgg)
class EggSandwich(Item):
    pass
