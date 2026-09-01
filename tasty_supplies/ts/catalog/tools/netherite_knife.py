from ts import smithing

from ._tool import Knife
from .diamond_knife import DiamondKnife


@smithing(base=DiamondKnife, addition="netherite_ingot")
class NetheriteKnife(Knife):
    damage = 4.5
    durability = 2032
