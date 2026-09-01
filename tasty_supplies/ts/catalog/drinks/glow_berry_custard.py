from ts import potion_effect, remainder

from ._drink import Drink


@potion_effect("glowing", 3600)
class GlowBerryCustard(Drink):
    ingredients = ["glow_berries", "milk_bucket", "egg", "sugar"]


@remainder("goat_horn")
class GlowBerryCustardHorn(GlowBerryCustard):
    container = "goat_horn"
