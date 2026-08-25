from ts import food

from ..ingredients.guardian_tail import GuardianTail
from ._roll import Roll


@food(8, 10.2)
class GuardianRoll(Roll):
    filling = GuardianTail
