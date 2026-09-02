from ts import potion_effect
from ts.catalog.ingredients.rice import Rice

from ._drink import AlcoholDrink


@potion_effect("nausea", 300)
class Sake(AlcoholDrink):
    reagent = Rice