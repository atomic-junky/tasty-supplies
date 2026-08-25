from ts import Item, bases, cooked, food


@food(2, 1.4)
class Tentacle(Item):
    base = bases.TENTACLE


@food(4, 3.8)
@cooked(Tentacle, time=250, xp=0.2)
class CookedTentacle(Item):
    base = bases.COOKED_TENTACLE
