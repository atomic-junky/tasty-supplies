from ts import apply_effect

from ._pie import Pie, PieSlice


@apply_effect("glowing", 3600)
class GlowBerryPie(Pie):
    top = "glow_berries"
    middle = "sugar"
    sides = "milk_bucket"


@apply_effect("glowing", 900, 1)
class GlowBerryPieSlice(PieSlice):
    source = GlowBerryPie
