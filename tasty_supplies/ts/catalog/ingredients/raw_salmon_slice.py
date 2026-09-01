from ts import Item, bases, cut, food


@food(1, 0.8)
@cut("salmon", count=2)
class RawSalmonSlice(Item):
    base = bases.RAW_SALMON_SLICE
