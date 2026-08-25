from ts import apply_effect

from ._pie import Pie, PieSlice


@apply_effect("speed", 3600)
class SweetBerryCheesecake(Pie):
    top = "sweet_berries"
    middle = "sweet_berries"
    sides = "milk_bucket"


@apply_effect("speed", 900, 1)
class SweetBerryCheesecakeSlice(PieSlice):
    source = SweetBerryCheesecake
