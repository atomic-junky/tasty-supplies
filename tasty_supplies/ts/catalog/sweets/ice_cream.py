from ts import Item, food, shapeless, stack

from ..ingredients.ice_cream_cone import IceCreamCone


@food(4, 3.6)
@stack(16)
@shapeless("snowball", "sugar", IceCreamCone)
class IceCream(Item):
    pass
