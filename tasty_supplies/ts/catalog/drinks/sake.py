from ts import apply_effect
from ts.catalog.ingredients.rice import Rice

from ._drink import AlcoholDrink


@apply_effect("nausea", 300)
class Sake(AlcoholDrink):
    reagent = Rice