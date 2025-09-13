from . import TSContext


class Category:
    def __init__(self, category_name=""):
        pass

    def register(self, ctx: TSContext):
        self.generate(ctx)
        ctx.showcase_items.append("\n")

    def generate(self, ctx: TSContext):
        pass
