from ts import Item, food, remainder, shapeless

from ..ingredients.pasta import Pasta
from ..ingredients.raw_salmon_slice import RawSalmonSlice


@food(10, 14.2)
@remainder("bowl")
@shapeless("bowl", Pasta, RawSalmonSlice, "dried_kelp", "seagrass")
class SeafoodPasta(Item):
    pass
