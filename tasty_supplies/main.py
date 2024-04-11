from beet import PngFile, Context


def build_resource_pack(ctx: Context):
    ctx.assets.icon = PngFile(source_path="tasty_supplies/pack.png")