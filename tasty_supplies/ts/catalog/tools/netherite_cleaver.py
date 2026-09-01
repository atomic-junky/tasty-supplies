from ts import smithing

from ._tool import Cleaver
from .diamond_cleaver import DiamondCleaver


@smithing(base=DiamondCleaver, addition="netherite_ingot")
class NetheriteCleaver(Cleaver):
    damage = 9
    speed = 1.2
    durability = 3046
