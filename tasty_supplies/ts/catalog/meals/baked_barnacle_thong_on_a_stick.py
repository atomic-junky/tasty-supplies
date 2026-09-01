from ts import Item, apply_effect, food, shaped

from ..ingredients.barnacle_thong import CookedBarnacleThong


@food(12, 14.8)
@apply_effect("water_breathing", 3600)
@shaped(["T", "s"], T=CookedBarnacleThong, s="stick")
class BakedBarnacleThongOnAStick(Item):
    pass
