from ts import potion_effect, remainder

from ._drink import Drink


@potion_effect("regeneration", 600)
class HotCocoa(Drink):
    ingredients = ["cocoa_beans", "cocoa_beans", "milk_bucket", "sugar"]


@remainder("goat_horn")
class HotCocoaHorn(HotCocoa):
    container = "goat_horn"
