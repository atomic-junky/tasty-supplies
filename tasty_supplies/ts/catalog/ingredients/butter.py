from ts import Item, bases, consume_effect, food, shapeless


@food(2, 1.2)
@consume_effect("clear_all_effects")
@shapeless("milk_bucket")
class Butter(Item):
    base = bases.BUTTER
