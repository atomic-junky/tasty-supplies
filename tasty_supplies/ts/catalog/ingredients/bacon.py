from ts import Item, bases, cooked, cut, food


@food(1.5, 0.3)
@cut("porkchop", count=2)
class RawBacon(Item):
    base = bases.RAW_BACON


@food(4, 6.4)
@cooked(RawBacon, time=150, xp=0.2)
class CookedBacon(Item):
    base = bases.COOKED_BACON
