from ts import Item, food, shapeless

from .cheese import CheeseSlice


@food(14, 20.8)
@shapeless("bread", "cooked_beef", CheeseSlice, "kelp")
class Cheeseburger(Item):
    pass
