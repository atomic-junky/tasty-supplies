from ts import Item, food, shapeless


@food(10, 17.2)
@shapeless("bread", "cooked_rabbit", "carrot", "kelp")
class RabbitBurger(Item):
    pass
