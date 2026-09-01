from ts import food

from ._skewer import Skewer


@food(6, 7.2)
class MushroomSkewer(Skewer):
    top = "brown_mushroom"
    bottom = "red_mushroom"
