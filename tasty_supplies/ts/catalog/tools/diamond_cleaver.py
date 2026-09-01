from ts import bases

from ._tool import Cleaver


class DiamondCleaver(Cleaver):
    base = bases.DIAMOND_CLEAVER
    material = "diamond"
    damage = 8
    speed = 1.2
    durability = 2341
