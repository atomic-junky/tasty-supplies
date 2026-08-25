from ts import Item, apply_effect, bases, food, rarity


@food(2, 1.6)
@apply_effect("mining_fatigue", 600)
@rarity("rare")
class GuardianTail(Item):
    base = bases.GUARDIAN_TAIL
