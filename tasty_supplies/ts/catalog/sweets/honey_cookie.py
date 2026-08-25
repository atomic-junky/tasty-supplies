from ts import Item, food, shaped


@food(2, 0.4)
@shaped(["whw"], h="honey_bottle", w="wheat")
class HoneyCookie(Item):
    pass
