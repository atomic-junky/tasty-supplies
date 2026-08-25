from ts import Item, food, shapeless


@food(8, 10.8)
@shapeless("baked_potato", "cooked_beef", "carrot", "milk_bucket")
class StuffedPotato(Item):
    pass
