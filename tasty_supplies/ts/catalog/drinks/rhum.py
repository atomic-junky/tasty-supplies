from ts import apply_effect

from ._drink import AlcoholDrink


@apply_effect("nausea", 300)
class Rhum(AlcoholDrink):
    reagent = "sugar_cane"