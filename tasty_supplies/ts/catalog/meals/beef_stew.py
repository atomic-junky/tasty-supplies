from ts import Item, bases, food, remainder, shapeless


@food(10, 12)
@remainder("bowl")
@shapeless("bowl", "cooked_beef", "carrot", "baked_potato")
class BeefStew(Item):
    base = bases.RABBIT_STEW
