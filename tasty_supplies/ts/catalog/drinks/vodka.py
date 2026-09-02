from ts import apply_effect
from ._drink import AlcoholDrink


@apply_effect("nausea", 300)
class Vodka(AlcoholDrink):
    reagent = "potato"