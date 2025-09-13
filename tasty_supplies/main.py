import json
from beet import PngFile, Context, Model, ItemModel

from core import log
from generator import generate
from core import TSContext


def build_pack(ctx: Context):
    ctx.assets.icon = PngFile(source_path="tasty_supplies/pack.png")

    ctx = TSContext(ctx)

    build_item_models(ctx)
    generate(ctx)


def build_item_models(ctx: TSContext):
    pack = ctx.assets
    for texture in ctx.assets.textures:
        item_name = texture.split("/")[1]
        if pack["tasty_supplies"].models.get(f"item/{item_name}"):
            continue

        json_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"tasty_supplies:item/{item_name}"},
        }
        model = Model(json.dumps(json_model), f"{item_name}.json")
        pack["tasty_supplies"].models[f"item/{item_name}"] = model
        pack["tasty_supplies"].item_models[item_name] = ItemModel(
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "tasty_supplies:item/" + item_name,
                }
            }
        )
