from ts import Item, food, remainder, shapeless

from ..ingredients.pasta import Pasta


@food(10, 10.6)
@remainder("bowl")
@shapeless("bowl", Pasta, "beetroot", "beetroot")
class BeetrootPasta(Item):
    pass
