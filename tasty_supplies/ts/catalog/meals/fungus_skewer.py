from ts import apply_effect, food

from ._skewer import Skewer


@food(5, 6)
@apply_effect("nausea", 600)
class FungusSkewer(Skewer):
    top = "warped_fungus"
    bottom = "crimson_fungus"
