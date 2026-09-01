from ts import Item, food, shapeless


@food(11, 16.4)
@shapeless("bread", "cooked_beef", "kelp")
class Hamburger(Item):
    pass
