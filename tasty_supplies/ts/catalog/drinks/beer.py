from ts import apply_effect

from ._drink import AlcoholDrink


@apply_effect("nausea", 300)
class Beer(AlcoholDrink):
    reagent = "wheat"


@apply_effect("nausea", 300)
class BeerHorn(AlcoholDrink):
    reagent = "wheat"
    container = "goat_horn"