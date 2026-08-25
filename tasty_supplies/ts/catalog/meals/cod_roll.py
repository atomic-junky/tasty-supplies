from ts import food

from ..ingredients.raw_cod_slice import RawCodSlice
from ._roll import Roll


@food(7, 9.4)
class CodRoll(Roll):
    filling = RawCodSlice
