from ts import potion_effect

from ._drink import AlcoholDrink


@potion_effect("nausea", 300)
class Beer(AlcoholDrink):
    reagent = "wheat"


@potion_effect("nausea", 300)
class BeerHorn(AlcoholDrink):
    reagent = "wheat"
    container = "goat_horn"