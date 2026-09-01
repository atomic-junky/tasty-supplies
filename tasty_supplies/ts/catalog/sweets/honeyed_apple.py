from ts import Item, food, shapeless


@food(6, 8.6)
@shapeless("apple", "honey_bottle")
class HoneyedApple(Item):
    pass
