from ts import potion_effect, remainder

from ._drink import Drink


@potion_effect("instant_health")
class MelonJuice(Drink):
    ingredients = ["melon_slice", "melon_slice", "melon_slice", "melon_slice", "sugar"]


@remainder("goat_horn")
class MelonJuiceHorn(MelonJuice):
    container = "goat_horn"
