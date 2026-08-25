from ts import Item, apply_effect, bases, cooked, food, rarity


@food(1, 0.8)
@apply_effect("nausea", 250)
@rarity("uncommon")
class BarnacleThong(Item):
    base = bases.BARNACLE_THONG


@food(2, 2.6)
@rarity("uncommon")
@cooked(BarnacleThong, time=200, xp=0.2)
class CookedBarnacleThong(Item):
    base = bases.COOKED_BARNACLE_THONG
