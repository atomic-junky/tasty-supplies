from ts import apply_effect

from ._pie import Pie, PieSlice


@apply_effect("slow_falling", 3600, 1)
class CherryBlossomPie(Pie):
    top = "cherry_leaves"
    middle = "milk_bucket"
    sides = "honeycomb"


@apply_effect("slow_falling", 900, 1)
class CherryBlossomPieSlice(PieSlice):
    source = CherryBlossomPie
