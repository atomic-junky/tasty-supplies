from ts import Item, bases, cut, food


@food(1, 0.8)
@cut("cod", count=2)
class RawCodSlice(Item):
    base = bases.RAW_COD_SLICE
