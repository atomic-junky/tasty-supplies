from ts import Item, bases, food, shapeless


@food(2, 0.8)
@shapeless("wheat", "wheat", "wheat", "egg")
@shapeless("wheat", "wheat", "wheat", "water_bucket")
class WheatDough(Item):
    base = bases.WHEAT_DOUGH
