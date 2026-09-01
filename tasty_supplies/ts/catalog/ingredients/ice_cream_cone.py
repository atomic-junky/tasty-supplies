from ts import Item, food, shaped


@food(2, 0.4)
@shaped(["W", "W", "W"], W="wheat", count=3)
class IceCreamCone(Item):
    pass
