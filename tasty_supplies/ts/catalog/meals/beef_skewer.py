from ts import Item, food, shaped


@food(16, 25.6)
@shaped(["b", "b", "s"], b="cooked_beef", s="stick")
class BeefSkewer(Item):
    pass
