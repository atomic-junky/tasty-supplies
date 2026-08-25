from ts import Item, food, shaped


@food(2, 0.4)
@shaped(["wbw"], b="sweet_berries", w="wheat")
class SweetBerryCookie(Item):
    pass
