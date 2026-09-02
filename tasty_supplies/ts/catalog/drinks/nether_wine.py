from ts import potion_effect

from ._drink import AlcoholDrink


@potion_effect("nausea", 300)
class NetherWine(AlcoholDrink):
    reagent = "nether_wart"