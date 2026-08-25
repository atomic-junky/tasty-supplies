from ts import Item, food, shapeless


@food(13, 18.4)
@shapeless("bread", "cooked_cod", "kelp")
class FishBurger(Item):
    pass
