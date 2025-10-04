import os
from typing import List
from beet import Function, Recipe
from PIL import Image

from .result import Result
from .context import TSContext
from .tools import to_absolute_path


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

    def _to_json(self) -> dict:
        raise NotImplementedError("Subclasses must implement this method.")


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
    def __init__(self, ingredient: str, result: Result, suffix=""):
        self.ingredient = ingredient
        self.result = result
        super().__init__("none", result, suffix)

    def _register(self, item_name: str, base_item: str, ctx: TSContext) -> dict:
        recipe_path: str = f"tasty_supplies:cutting_board/recipes/{item_name}"
        result_item: dict = self.result._to_json(item_name, base_item)
        is_vanilla_ingredient: bool = False

        for recipe in ctx.vanilla.data.recipes.keys():
            if self.ingredient in recipe:
                is_vanilla_ingredient = True
                break

        ctx.data[recipe_path] = Function(
            [
                "summon minecraft:item ~ ~.5 ~ {Item:%s}" % result_item,
                "kill @s",
            ]
        )
        f_cut_item = ctx.data["tasty_supplies"].functions.get("cutting_board/cut_item")
        if not is_vanilla_ingredient:
            f_cut_item.append(
                Function(
                    'execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/%s"]}}} run function %s'
                    % (self.ingredient, recipe_path)
                )
            )
        else:
            f_cut_item.append(
                Function(
                    'execute if data entity @s item{id: "%s"} run function %s'
                    % (to_absolute_path(self.ingredient), recipe_path)
                )
            )

    def _to_json(self) -> dict:
        return {}
