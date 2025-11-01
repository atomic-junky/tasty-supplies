"""New recipe system that is independent from item creation.

This module provides recipe classes that can reference both vanilla and custom items
as ingredients and results. Recipes are created separately from items and generate
the actual .json recipe files.
"""

from typing import List, Union, Dict, Any
from beet import Function, Recipe as BeetRecipe
from .context import TSContext
from .item import Item
from core.utils import to_absolute_path
from core.logger import log


def _process_ingredient(ingredient: Union[str, Item, dict]) -> Union[str, dict]:
    """Convert an ingredient to the correct format for recipes.

    Args:
        ingredient: Can be a string (vanilla item), Item object (custom), or dict (explicit format)

    Returns:
        String path or dict ingredient data
    """
    if isinstance(ingredient, Item):
        return ingredient.to_ingredient()
    elif isinstance(ingredient, dict):
        return ingredient
    else:
        return to_absolute_path(str(ingredient))


def _process_result(result: Union[str, Item, dict], count: int = 1) -> dict:
    """Convert a result to the correct format for recipes.

    Args:
        result: Can be a string (vanilla item), Item object (custom), or dict (explicit format)
        count: Number of items to produce

    Returns:
        Dict with result data
    """
    if isinstance(result, Item):
        return result.to_result(count=count)
    elif isinstance(result, dict):
        return result
    else:
        # Vanilla item
        return {"id": to_absolute_path(str(result)), "count": count}


class Recipe:
    """Base class for all recipe types.

    Recipes are independent from items and can reference both vanilla
    and custom items as ingredients and results.
    """

    def __init__(
        self,
        recipe_id: str,
        result: Union[str, Item, dict],
        category: str = "misc",
        result_count: int = 1,
    ):
        """Initialize a recipe.

        Args:
            recipe_id: Unique identifier for this recipe
            result: The output item (vanilla string, Item object, or explicit dict)
            category: Recipe category for the recipe book
            result_count: Number of items to produce
        """
        self.recipe_id = recipe_id
        self.result = result
        self.category = category
        self.result_count = result_count

    def register(self, ctx: TSContext):
        """Register this recipe with the Beet context.

        Args:
            ctx: The Tasty Supplies context
        """
        recipe_json = self._to_json()
        ctx.data["tasty_supplies"].recipes[self.recipe_id] = BeetRecipe(recipe_json)
        log.debug(f"Registered recipe '{self.recipe_id}'")

    def _to_json(self) -> dict:
        """Convert this recipe to JSON format.

        Returns:
            Dict with complete recipe data
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _get_result_json(self) -> dict:
        """Get the result portion of the recipe JSON.

        Returns:
            Dict with result data
        """
        return _process_result(self.result, count=self.result_count)


class ShapelessRecipe(Recipe):
    """A shapeless crafting recipe.

    Ingredients can be placed in any arrangement in the crafting grid.
    """

    def __init__(
        self,
        ingredients: List[Union[str, Item, dict]],
        result: Union[str, Item, dict],
        recipe_id: str = "",
        category: str = "misc",
        result_count: int = 1,
    ):
        """Initialize a shapeless recipe.

        Args:
            ingredients: List of ingredients (vanilla, custom items, or dicts)
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            category: Recipe category
            result_count: Number of items to produce
        """
        super().__init__(recipe_id, result, category, result_count)
        self.ingredients = ingredients

    def _to_json(self) -> dict:
        return {
            "type": "minecraft:crafting_shapeless",
            "category": self.category,
            "ingredients": [_process_ingredient(ing) for ing in self.ingredients],
            "result": self._get_result_json(),
        }


class ShapedRecipe(Recipe):
    """A shaped crafting recipe.

    Ingredients must be placed in a specific pattern in the crafting grid.
    """

    def __init__(
        self,
        pattern: List[str],
        key: Dict[str, Union[str, Item, dict]],
        result: Union[str, Item, dict],
        recipe_id: str = "",
        category: str = "misc",
        result_count: int = 1,
    ):
        """Initialize a shaped recipe.

        Args:
            pattern: List of pattern strings (e.g., ["AAA", "ABA", "AAA"])
            key: Dict mapping pattern characters to ingredients
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            category: Recipe category
            result_count: Number of items to produce
        """
        super().__init__(recipe_id, result, category, result_count)
        self.pattern = pattern
        self.key = key

    def _to_json(self) -> dict:
        # Process the key ingredients
        processed_key = {}
        for char, ingredient in self.key.items():
            processed_key[char] = _process_ingredient(ingredient)

        return {
            "type": "minecraft:crafting_shaped",
            "category": self.category,
            "pattern": self.pattern,
            "key": processed_key,
            "result": self._get_result_json(),
        }


class SmeltingRecipe(Recipe):
    """A smelting/cooking recipe (furnace, blast furnace, smoker, campfire).

    Supports all cooking types through the cooking_type parameter.
    """

    def __init__(
        self,
        ingredient: Union[str, Item, dict],
        result: Union[str, Item, dict],
        recipe_id: str = "",
        cooking_type: str = "smelting",
        experience: float = 0.1,
        cooking_time: int = 200,
        category: str = "misc",
        result_count: int = 1,
    ):
        """Initialize a smelting/cooking recipe.

        Args:
            ingredient: The input item
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            cooking_type: Type of cooking ("smelting", "blasting", "smoking", "campfire_cooking")
            experience: XP awarded when collected
            cooking_time: Time in ticks (20 ticks = 1 second)
            category: Recipe category
            result_count: Number of items to produce
        """
        super().__init__(recipe_id, result, category, result_count)
        self.ingredient = ingredient
        self.cooking_type = cooking_type
        self.experience = experience
        self.cooking_time = cooking_time

    def _to_json(self) -> dict:
        recipe_data = {
            "type": f"minecraft:{self.cooking_type}",
            "ingredient": _process_ingredient(self.ingredient),
            "result": self._get_result_json(),
            "cookingtime": self.cooking_time,
        }

        # Campfire cooking doesn't have experience or category
        if self.cooking_type != "campfire_cooking":
            recipe_data["experience"] = self.experience
            recipe_data["category"] = self.category

        return recipe_data


class AutoCookingRecipe:
    """Automatically creates smelting, blasting, smoking, and campfire recipes.

    This is a convenience class that generates all four cooking variations
    with appropriate time adjustments.
    """

    def __init__(
        self,
        ingredient: Union[str, Item, dict],
        result: Union[str, Item, dict],
        base_recipe_id: str = "",
        base_cooking_time: int = 200,
        experience: float = 0.1,
        category: str = "misc",
        result_count: int = 1,
    ):
        """Initialize auto-cooking recipes.

        Args:
            ingredient: The input item
            result: The output item
            base_recipe_id: Base identifier (suffixes will be added, auto-generated if empty)
            base_cooking_time: Base time in ticks (others calculated from this)
            experience: XP awarded
            category: Recipe category
            result_count: Number of items to produce
        """
        # Store the base_recipe_id for the bucket to potentially override
        self.base_recipe_id = base_recipe_id

        self.recipes = [
            SmeltingRecipe(
                ingredient,
                result,
                f"{base_recipe_id}_blasting" if base_recipe_id else "",
                "blasting",
                experience,
                int(base_cooking_time * 0.5),
                category,
                result_count,
            ),
            SmeltingRecipe(
                ingredient,
                result,
                f"{base_recipe_id}_smoking" if base_recipe_id else "",
                "smoking",
                experience,
                int(base_cooking_time * 0.5),
                category,
                result_count,
            ),
            SmeltingRecipe(
                ingredient,
                result,
                f"{base_recipe_id}_campfire" if base_recipe_id else "",
                "campfire_cooking",
                0.0,
                int(base_cooking_time * 3),
                category,
                result_count,
            ),
        ]

    def register(self, ctx: TSContext):
        """Register all cooking recipe variants.

        Args:
            ctx: The Tasty Supplies context
        """
        for recipe in self.recipes:
            recipe.register(ctx)


class SmithingTransformRecipe(Recipe):
    """A smithing table transformation recipe.

    Used for upgrading items with smithing templates.
    """

    def __init__(
        self,
        template: Union[str, Item, dict],
        base: Union[str, Item, dict],
        addition: Union[str, Item, dict],
        result: Union[str, Item, dict],
        recipe_id: str = "",
        result_count: int = 1,
    ):
        """Initialize a smithing transform recipe.

        Args:
            template: The smithing template required
            base: The base item to upgrade
            addition: The material to add
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            result_count: Number of items to produce
        """
        super().__init__(recipe_id, result, "", result_count)
        self.template = template
        self.base = base
        self.addition = addition

    def _to_json(self) -> dict:
        return {
            "type": "minecraft:smithing_transform",
            "template": _process_ingredient(self.template),
            "base": _process_ingredient(self.base),
            "addition": _process_ingredient(self.addition),
            "result": self._get_result_json(),
        }


class CuttingBoardRecipe:
    """A custom cutting board recipe for the mod.

    This creates function files rather than standard recipe JSON files.
    """

    def __init__(
        self,
        ingredient: Union[str, Item, dict],
        result: Union[str, Item, dict],
        recipe_id: str = "",
        result_count: int = 1,
    ):
        """Initialize a cutting board recipe.

        Args:
            ingredient: The input item
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            result_count: Number of items to produce
        """
        self.recipe_id = recipe_id
        self.ingredient = ingredient
        self.result = result
        self.result_count = result_count

    def register(self, ctx: TSContext):
        """Register this cutting board recipe.

        Args:
            ctx: The Tasty Supplies context
        """
        recipe_path = f"tasty_supplies:cutting_board/recipes/{self.recipe_id}"
        result_json = _process_result(self.result, count=self.result_count)

        # Create the function that spawns the result item
        ctx.data[recipe_path] = Function(
            [
                f"summon minecraft:item ~ ~.5 ~ {{Item:{result_json}}}",
                "kill @s",
            ]
        )

        # Add to the cutting board's main function
        f_cut_item = ctx.data["tasty_supplies"].functions.get("cutting_board/cut_item")

        # Determine if ingredient is vanilla or custom
        ingredient_check = self._get_ingredient_check()
        f_cut_item.append(
            Function(
                f"execute if data entity @s item{ingredient_check} run function {recipe_path}"
            )
        )

        log.debug(f"Registered cutting board recipe '{self.recipe_id}'")

    def _get_ingredient_check(self) -> str:
        """Get the NBT check string for the ingredient.

        Returns:
            String with the NBT check for /execute if data
        """
        if isinstance(self.ingredient, Item):
            return (
                f'{{id: "minecraft:{self.ingredient.base_item}", '
                f'components: {{"minecraft:custom_model_data": '
                f'{{"strings": ["tasty_supplies/{self.ingredient.name}"]}}}}}}'
            )
        elif isinstance(self.ingredient, dict):
            # Custom dict format - would need more complex handling
            return str(self.ingredient)
        else:
            # Vanilla item
            return f'{{id: "{to_absolute_path(str(self.ingredient))}"}}'
