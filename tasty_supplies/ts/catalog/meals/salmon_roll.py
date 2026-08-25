from ts import food

from ..ingredients.raw_salmon_slice import RawSalmonSlice
from ._roll import Roll


@food(7, 9.4)
class SalmonRoll(Roll):
    filling = RawSalmonSlice
