from ts import consume_effect, cooldown

from ._pie import Pie, PieSlice


@consume_effect("teleport_randomly", diameter=32)
@cooldown(2.0, group="chorus_pie")
class ChorusPie(Pie):
    top = "chorus_fruit"
    middle = "sugar"
    sides = "milk_bucket"


@consume_effect("teleport_randomly", diameter=8)
@cooldown(1.0, group="chorus_pie")
class ChorusPieSlice(PieSlice):
    source = ChorusPie
