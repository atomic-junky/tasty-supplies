from ts import Item, food, remainder, shapeless

from ..ingredients.pasta import Pasta
from ..ingredients.raw_cod_slice import RawCodSlice
from ..ingredients.raw_salmon_slice import RawSalmonSlice


@food(8, 9.4)
@remainder("bowl")
@shapeless("bowl", Pasta, RawCodSlice, "ink_sac", "beetroot")
@shapeless("bowl", Pasta, RawSalmonSlice, "ink_sac", "beetroot")
class InkPasta(Item):
    pass
