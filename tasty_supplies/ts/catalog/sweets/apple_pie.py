from ._pie import Pie, PieSlice


class ApplePie(Pie):
    top = "wheat"
    middle = "apple"
    sides = "sugar"


class ApplePieSlice(PieSlice):
    source = ApplePie
