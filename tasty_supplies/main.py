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

    generate(ts_ctx)
