from ts import potion_effect, remainder

from ._drink import Drink


@potion_effect("absorption", 1800, 1)
class AppleCider(Drink):
    ingredients = ["apple", "apple", "sugar"]


@remainder("goat_horn")
class AppleCiderHorn(AppleCider):
    container = "goat_horn"
