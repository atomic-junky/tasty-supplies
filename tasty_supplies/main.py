"""Main entry point for Tasty Supplies datapack generation.

This module provides the build_pack function that is called by Beet
to generate the complete datapack.
"""

import json
from typing import Dict, Any
from beet import PngFile, Context, Model, ItemModel

from core import TSContext
from generator import generate


def build_pack(ctx: Context) -> None:
    """Build the Tasty Supplies datapack.

    This is the main entry point called by Beet to generate all datapack resources.

    Args:
        ctx: The Beet context
    """
    ctx.assets.icon = PngFile(source_path="tasty_supplies/pack.png")

    ts_ctx: TSContext = TSContext(ctx)

    build_item_models(ts_ctx)
    generate(ts_ctx)


def build_item_models(ctx: TSContext) -> None:
    """Build item models for all textures in the assets.

    Automatically generates model and item_model files for each texture
    found in the assets that doesn't already have a model.

    Args:
        ctx: The Tasty Supplies context
    """
    pack = ctx.assets
    for texture in ctx.assets.textures:
        item_name: str = texture.split("/")[1]
        if pack["tasty_supplies"].models.get(f"item/{item_name}"):
            continue

        json_model: Dict[str, Any] = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"tasty_supplies:item/{item_name}"},
        }
        model: Model = Model(json.dumps(json_model), f"{item_name}.json")
        pack["tasty_supplies"].models[f"item/{item_name}"] = model
        pack["tasty_supplies"].item_models[item_name] = ItemModel(
            {
                "model": {
                    "type": "minecraft:model",
                    "model": f"tasty_supplies:item/{item_name}",
                }
            }
        )
