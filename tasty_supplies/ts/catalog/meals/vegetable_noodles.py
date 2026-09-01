from ts import Item, food, remainder, shapeless

from ..ingredients.pasta import Pasta


@food(12, 12.6)
@remainder("bowl")
@shapeless("bowl", Pasta, "carrot", "brown_mushroom", "kelp", "potato")
@shapeless("bowl", Pasta, "carrot", "brown_mushroom", "kelp", "carrot")
@shapeless("bowl", Pasta, "carrot", "brown_mushroom", "kelp", "beetroot")
class VegetableNoodles(Item):
    pass
