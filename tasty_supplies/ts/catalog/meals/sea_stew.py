from ts import Item, food, remainder, shapeless

from ..ingredients.tentacle import CookedTentacle


@food(12, 10.2)
@remainder("bowl")
@shapeless("bowl", CookedTentacle, "cooked_cod", "#tasty_supplies:water")
class SeaStew(Item):
    pass
