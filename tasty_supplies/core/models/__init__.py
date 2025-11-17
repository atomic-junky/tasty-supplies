from .context import TSContext
from .category import Category
from .advancement import Advancement, AdvancementIcon, AdvancementRewards, ADVANCEMENT_TYPE

# Recipe system (independent from items)
from .recipe import (
    Recipe,
    ShapedRecipe,
    ShapelessRecipe,
    SmeltingRecipe,
    AutoCookingRecipe,
    SmithingTransformRecipe,
    CuttingBoardRecipe,
)

# Item system (independent from recipes)
from .item import Item, BlockItem
