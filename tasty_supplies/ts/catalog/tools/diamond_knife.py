from ts import bases

from ._tool import Knife


class DiamondKnife(Knife):
    base = bases.DIAMOND_KNIFE
    material = "diamond"
    damage = 4
    durability = 1561
