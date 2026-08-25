from ts import Item, food, shaped

from ..ingredients.tentacle import CookedTentacle


@food(14, 16.8)
@shaped(["T", "T", "s"], T=CookedTentacle, s="stick")
class BakedTentacleOnAStick(Item):
    pass
