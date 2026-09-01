from ts import Item, bases, cooked, cut, food


@cut("wheat", count=4)
class Rice(Item):
    base = bases.RICE


@food(2, 3.2)
@cooked(Rice, time=150, xp=0.25)
class CookedRice(Item):
    base = bases.COOKED_RICE
