from ts import Item, food, shapeless

from ..ingredients.tentacle import CookedTentacle


@food(14, 19.6)
@shapeless("bread", CookedTentacle, CookedTentacle, "kelp")
class SquidSandwich(Item):
    pass
