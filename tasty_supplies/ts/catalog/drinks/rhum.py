from ts import potion_effect

from ._drink import AlcoholDrink


@potion_effect("nausea", 300)
class Rhum(AlcoholDrink):
    reagent = "sugar_cane"