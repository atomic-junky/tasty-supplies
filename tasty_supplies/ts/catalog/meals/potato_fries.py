from ts import Item, cut, food


@food(1.5, 1.5)
@cut("baked_potato", count=4)
class PotatoFries(Item):
    pass
