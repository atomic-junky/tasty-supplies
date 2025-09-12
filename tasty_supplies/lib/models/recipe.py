import math
import os
from typing import List
from beet import Recipe, Texture
from PIL import Image

from .result import Result
from .context import TSContext
from .tools import to_absolute_path


CRAFTING_TABLE_BG = Image.open(
    "./docs/_media/recipes/blank_recipes/blank_crafting_table_recipe.png"
).convert("RGBA")
FURNACE_TABLE_BG = Image.open(
    "./docs/_media/recipes/blank_recipes/blank_furnace_recipe.png"
).convert("RGBA")
CUTTING_BOARD_BG = Image.open(
    "./docs/_media/recipes/blank_recipes/blank_cutting_board_recipe.png"
).convert("RGBA")
ITEMS_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/item"
BLOCK_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/block"
RECIPES_RESULT = "./docs/_media/recipes"


class _Recipe:
    def __init__(
        self, category: str = "misc", result: Result = Result(), suffix: str = ""
    ):
        self.category = category
        self.result = result
        self.suffix = suffix

    def _register(self, item_name: str, base_item: str, ctx: TSContext) -> dict:
        result = self._to_json() | {
            "result": self.result._to_json(item_name, base_item)
        }

        ctx.data["tasty_supplies"].recipes[f"{item_name}{self.suffix}"] = Recipe(result)

        im: Image = self._create_recipe_image(ctx, item_name)
        im.save(os.path.join(RECIPES_RESULT, f"{item_name}.png"))

    def _to_json(self) -> dict:
        raise NotImplementedError("Subclasses must implement this method.")

    def _create_recipe_image(
        self,
        ctx: TSContext,
        item_name: str,
    ):
        pass


class FakeRecipe(_Recipe):
    pass


class ShapelessRecipe(_Recipe):
    def __init__(
        self,
        ingredients: list,
        category: str = "misc",
        result: Result = Result(),
        suffix: str = "",
    ):
        super().__init__(category, result, suffix)
        self.ingredients = ingredients

    def _to_json(self) -> dict:
        return {
            "type": "minecraft:crafting_shapeless",
            "category": self.category,
            "ingredients": [
                to_absolute_path(ingredient) for ingredient in self.ingredients
            ],
        }

    def _create_recipe_image(
        self,
        ctx: TSContext,
        item_name: str,
    ):
        im = _upscale(CRAFTING_TABLE_BG.copy(), 2)
        padding = (58, 32)

        ingredients = self.ingredients
        is_2x2 = len(ingredients) <= 4

        index = 0
        for item in ingredients:
            raw = math.floor(index / (2 if is_2x2 else 3))
            col = index - raw * (2 if is_2x2 else 3)

            texture = _get_item_texture(ctx, f"minecraft:{item}")
            mask = _create_a_mask(texture)

            im.paste(
                texture,
                (
                    padding[0] + col * (32 + 3) + col + 2,
                    padding[1] + raw * (32 + 3) + raw + 2,
                ),
                mask,
            )

            index += 1

        result_texture = _get_item_texture(ctx, item_name)
        mask = _create_a_mask(result_texture)
        im.paste(result_texture, (248, 70), mask)

        return im


class ShapedRecipe(_Recipe):
    def __init__(
        self,
        key: dict,
        pattern: List[str],
        result: Result = Result(),
        category: str = "misc",
        suffix: str = "",
    ):
        super().__init__(category, result, suffix)
        self.key = key
        self.pattern = pattern

    def _to_json(self) -> dict:
        return {
            "type": "minecraft:crafting_shaped",
            "category": self.category,
            "key": self.key,
            "pattern": self.pattern,
        }

    def _create_recipe_image(
        self,
        ctx: TSContext,
        item_name: str,
    ):
        im = _upscale(CRAFTING_TABLE_BG.copy(), 2)
        padding = (58, 32)

        keys = self.key
        pattern = self.pattern

        min_raw = 0
        min_col = 0
        for line in pattern:
            if len(line) > 1:
                min_col = 0
                break
            min_col = 1

        if len(pattern) <= 1:
            min_raw = 1

        raw = min_raw
        col = min_col

        for line in pattern:
            for key in line:
                if not key in keys:
                    continue
                item = keys[key]

                texture = _get_item_texture(ctx, f"{item}")
                mask = _create_a_mask(texture)

                im.paste(
                    texture,
                    (
                        padding[0] + col * (32 + 3) + col + 2,
                        padding[1] + raw * (32 + 3) + raw + 2,
                    ),
                    mask,
                )

                col += 1
            raw += 1
            col = min_col

        result_texture = _get_item_texture(ctx, item_name)
        mask = _create_a_mask(result_texture)
        im.paste(result_texture, (248, 70), mask)

        return im


## Automatically create item recipes for blasting, smoking and campfire.
class AutoBakeRecipe(_Recipe):
    def __init__(
        self,
        ingredient: str,
        experience: float,
        cookingtime: int,
        category: str = "misc",
        result=Result(),
        suffix="",
    ):
        super().__init__(category, result, suffix)
        self._blasting_recipe = BlastingRecipe(
            ingredient=ingredient,
            experience=experience,
            cookingtime=cookingtime,
            result=result,
            suffix=suffix,
        )
        self._smoking_recipe = SmokingRecipe(
            ingredient=ingredient,
            experience=experience,
            cookingtime=cookingtime * 0.7,
            result=result,
            suffix=suffix,
        )
        self._campfire_recipe = CampfireRecipe(
            ingredient=ingredient,
            cookingtime=cookingtime * 1.3,
            result=result,
            suffix=suffix,
        )

    def _register(self, item_name: str, base_item: str, ctx: TSContext) -> dict:
        self._blasting_recipe._register(item_name, base_item, ctx)
        self._smoking_recipe._register(item_name, base_item, ctx)
        self._campfire_recipe._register(item_name, base_item, ctx)


class BlastingRecipe(_Recipe):
    def __init__(
        self,
        ingredient: str,
        experience: float,
        cookingtime: int,
        category: str = "misc",
        result: Result = Result(),
        suffix: str = "",
    ):
        super().__init__(category, result, suffix)
        self.ingredient = ingredient
        self.experience = experience
        self.cookingtime = cookingtime
        self.type = "blasting"

    def _to_json(self) -> dict:
        return {
            "type": f"minecraft:{self.type}",
            "category": self.category,
            "ingredient": to_absolute_path(self.ingredient),
            "experience": self.experience,
            "cookingtime": self.cookingtime,
        }

    def _create_recipe_image(
        self,
        ctx: TSContext,
        item_name: str,
    ):
        im = _upscale(FURNACE_TABLE_BG.copy(), 2)

        ingredient_texture = _get_item_texture(ctx, self.ingredient)
        mask = _create_a_mask(ingredient_texture)
        im.paste(ingredient_texture, (112, 34), mask)

        result_texture = _get_item_texture(ctx, item_name)
        mask = _create_a_mask(result_texture)
        im.paste(result_texture, (232, 70), mask)

        return im


class SmeltingRecipe(BlastingRecipe):
    def __init__(
        self,
        ingredient: str,
        experience: float,
        cookingtime: int,
        category: str = "misc",
        result: Result = Result(),
        suffix: str = "",
    ):
        suffix += "_smelting"
        super().__init__(ingredient, experience, cookingtime, category, result, suffix)
        self.type = "smelting"


class SmokingRecipe(BlastingRecipe):
    def __init__(
        self,
        ingredient: str,
        experience: float,
        cookingtime: int,
        category: str = "misc",
        result: Result = Result(),
        suffix: str = "",
    ):
        suffix += "_smoking"
        super().__init__(ingredient, experience, cookingtime, category, result, suffix)
        self.type = "smoking"


class CampfireRecipe(BlastingRecipe):
    def __init__(
        self,
        ingredient: str,
        cookingtime: int,
        category: str = "misc",
        result: Result = Result(),
        suffix: str = "",
    ):
        suffix += "_campfire"
        super().__init__(ingredient, 0.0, cookingtime, category, result, suffix)
        self.type = "campfire_cooking"

    def _to_json(self) -> dict:
        return {
            "type": f"minecraft:{self.type}",
            "ingredient": to_absolute_path(self.ingredient),
            "cookingtime": self.cookingtime,
        }


class CuttingBoardRecipe(_Recipe):
    def __init__(self, ingredient: str, suffix=""):
        self.ingredient = ingredient
        super().__init__("none", Result(), suffix)

    def _register(self, item_name: str, base_item: str, ctx: TSContext) -> dict:
        im = self._create_recipe_image(ctx, item_name)
        im.save(os.path.join(RECIPES_RESULT, f"{item_name}.png"))

    def _to_json(self) -> dict:
        pass

    def _create_recipe_image(
        self,
        ctx: TSContext,
        item_name: str,
    ):
        im = _upscale(CUTTING_BOARD_BG.copy(), 2)

        ingredient_texture = _get_item_texture(ctx, self.ingredient)
        mask = _create_a_mask(ingredient_texture)
        im.paste(ingredient_texture, (112, 68), mask)

        result_texture = _get_item_texture(ctx, item_name)
        mask = _create_a_mask(result_texture)
        im.paste(result_texture, (232, 70), mask)

        return im


def _upscale(im, factor):
    return im.resize(tuple(i * factor for i in im.size), Image.Resampling.NEAREST)


def _get_item_texture(ctx: TSContext, item_name: str, upscale: bool = True):
    path = ""

    if "#" in item_name:
        item_name = item_name.removeprefix("minecraft:")
        item_name = item_name.removeprefix("#")
        tag = {}
        if item_name in ctx.vanilla.data.item_tags.keys():
            tag = ctx.vanilla.data.item_tags[item_name].data
        elif item_name in ctx.vanilla.data.block_tags.keys():
            tag = ctx.vanilla.data.block_tags[item_name].data
        elif item_name in ctx.data.item_tags.keys():
            tag = ctx.data.item_tags[item_name].data
        elif item_name in ctx.data.block_tags.keys():
            tag = ctx.data.block_tags[item_name].data

        if "values" in tag:
            return _get_item_texture(ctx, tag["values"][0])

        path = ctx.vanilla.assets.textures[f"minecraft:item/barrier"].source_path
    else:
        raw_name = item_name.removeprefix("minecraft:")
        texture_item_name = f"minecraft:item/{raw_name}"
        texture_block_name = f"minecraft:block/{raw_name}"

        if texture_item_name in ctx.vanilla.assets.textures.keys():
            path = ctx.vanilla.assets.textures[texture_item_name].source_path
        elif texture_block_name in ctx.vanilla.assets.textures.keys():
            path = ctx.vanilla.assets.textures[texture_block_name].source_path
        elif f"{item_name}.png" in os.listdir(ITEMS_LOCATION):
            path = os.path.join(ITEMS_LOCATION, f"{item_name}.png")
        elif f"{item_name}.png" in os.listdir(BLOCK_LOCATION):
            path = os.path.join(BLOCK_LOCATION, f"{item_name}.png")

    im = Image.open(path, "r")

    if upscale:
        im = _upscale(im, 2)

    return im


def _create_a_mask(im: Image):
    return im.convert("LA")
