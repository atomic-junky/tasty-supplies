from ts import Item, cut, food, shaped

from ..ingredients.rice import CookedRice


@food(10, 12.6)
@shaped(["rcr", "kkk"], k="dried_kelp", r=CookedRice, c="carrot")
class KelpRoll(Item):
    pass


@food(2.5, 6.2)
@cut(KelpRoll, count=4)
class KelpRollSlice(Item):
    pass
