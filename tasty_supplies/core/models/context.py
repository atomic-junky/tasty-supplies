from beet import Context
from beet.contrib.vanilla import Vanilla


class TSContext(Context):
    def __init__(self, ctx: Context):
        version: str = "1.21"
        self.__dict__ = ctx.__dict__.copy()
        self.vanilla = Vanilla(ctx=self, minecraft_version=version)
