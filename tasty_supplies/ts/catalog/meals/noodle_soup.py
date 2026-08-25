from ts import Item, food, remainder, shapeless

from ..ingredients.bacon import CookedBacon
from ..ingredients.pasta import Pasta


@food(12, 16.2)
@remainder("bowl")
@shapeless("bowl", Pasta, CookedBacon, "egg", "dried_kelp")
@shapeless("bowl", Pasta, "cooked_porkchop", "egg", "dried_kelp")
class NoodleSoup(Item):
    pass
