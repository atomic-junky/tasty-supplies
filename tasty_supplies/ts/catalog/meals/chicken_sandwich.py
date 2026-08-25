from ts import Item, food, shapeless


@food(12, 19.0)
@shapeless("bread", "cooked_chicken", "carrot", "kelp")
class ChickenSandwich(Item):
    pass
