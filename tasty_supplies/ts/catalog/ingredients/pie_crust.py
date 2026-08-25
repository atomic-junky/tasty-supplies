from ts import Item, bases, shaped

from .butter import Butter


@shaped(["WBW", " W "], W="wheat", B=Butter)
class PieCrust(Item):
    base = bases.PIE_CRUST
