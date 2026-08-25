from ts import Item, food, shapeless

from ..ingredients.bacon import CookedBacon


@food(14, 20.8)
@shapeless("bread", CookedBacon, CookedBacon, "kelp")
class BaconSandwich(Item):
    pass
