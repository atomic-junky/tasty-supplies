from ts import apply_effect

from ._pie import Pie, PieSlice


@apply_effect("speed", 3600, 1)
class ChocolatePie(Pie):
    top = "cocoa_beans"
    middle = "milk_bucket"
    sides = "sugar"


@apply_effect("speed", 900, 1)
class ChocolatePieSlice(PieSlice):
    source = ChocolatePie
