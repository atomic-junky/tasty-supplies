from beet import Context
from beet.contrib.vanilla import Vanilla


class TSContext(Context):
    def __init__(self, ctx: Context):
        self.__dict__ = ctx.__dict__.copy()
        self.vanilla = ctx.inject(Vanilla)
