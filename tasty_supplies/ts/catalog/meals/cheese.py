from ts import Item, bases, cooked, cut, food


@food(8, 5.6)
@cooked("milk_bucket", time=200, xp=0.5)
class Cheese(Item):
    pass


@food(2, 1.4)
@cut(Cheese, count=4)
class CheeseSlice(Item):
    base = bases.CHEESE_SLICE
