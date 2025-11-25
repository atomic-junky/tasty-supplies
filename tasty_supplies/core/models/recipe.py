"""New recipe system that is independent from item creation.

This module provides recipe classes that can reference both vanilla and custom items
as ingredients and results. Recipes are created separately from items and generate
the actual .json recipe files.
"""

from typing import List, Union, Dict, Any
from beet import Function, Recipe as BeetRecipe

from .context import TSContext
from .item import Item
from ..utils import to_absolute_path
from ..logger import log

# Type aliases for better readability
IngredientType = Union[str, Item, Dict[str, Any]]
ResultType = Union[str, Item, Dict[str, Any]]


def _process_ingredient(ingredient: IngredientType) -> Union[str, Dict[str, Any]]:
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


def _process_result(result: ResultType, count: int = 1) -> Dict[str, Any]:
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
        result: ResultType,
        category: str = "misc",
        result_count: int = 1,
    ) -> None:
        """Initialize a recipe.

        Args:
            recipe_id: Unique identifier for this recipe
            result: The output item (vanilla string, Item object, or explicit dict)
            category: Recipe category for the recipe book
            result_count: Number of items to produce
        """
        self.recipe_id: str = recipe_id
        self.result: ResultType = result
        self.category: str = category
        self.result_count: int = result_count

    def register(self, ctx: TSContext) -> None:
        """Register this recipe with the Beet context.

        Args:
            ctx: The Tasty Supplies context
        """
        recipe_json: Dict[str, Any] = self._to_json()
        ctx.data["tasty_supplies"].recipes[self.recipe_id] = BeetRecipe(recipe_json)
        log.debug(f"Registered recipe '{self.recipe_id}'")

    def _to_json(self) -> Dict[str, Any]:
        """Convert this recipe to JSON format.

        Returns:
            Dict with complete recipe data
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _get_result_json(self) -> Dict[str, Any]:
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
        ingredients: List[IngredientType],
        result: ResultType,
        recipe_id: str = "",
        category: str = "misc",
        result_count: int = 1,
    ) -> None:
        """Initialize a shapeless recipe.

        Args:
            ingredients: List of ingredients (vanilla, custom items, or dicts)
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            category: Recipe category
            result_count: Number of items to produce
        """
        super().__init__(recipe_id, result, category, result_count)
        self.ingredients: List[IngredientType] = ingredients

    def _to_json(self) -> Dict[str, Any]:
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
        key: Dict[str, IngredientType],
        result: ResultType,
        recipe_id: str = "",
        category: str = "misc",
        result_count: int = 1,
    ) -> None:
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
        self.pattern: List[str] = pattern
        self.key: Dict[str, IngredientType] = key

    def _to_json(self) -> Dict[str, Any]:
        # Process the key ingredients
        processed_key: Dict[str, Union[str, Dict[str, Any]]] = {}
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
        ingredient: IngredientType,
        result: ResultType,
        recipe_id: str = "",
        cooking_type: str = "smelting",
        experience: float = 0.1,
        cooking_time: int = 200,
        category: str = "misc",
        result_count: int = 1,
    ) -> None:
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
        self.ingredient: IngredientType = ingredient
        self.cooking_type: str = cooking_type
        self.experience: float = experience
        self.cooking_time: int = cooking_time

    def _to_json(self) -> Dict[str, Any]:
        recipe_data: Dict[str, Any] = {
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
        ingredient: IngredientType,
        result: ResultType,
        base_recipe_id: str = "",
        base_cooking_time: int = 200,
        experience: float = 0.1,
        category: str = "misc",
        result_count: int = 1,
    ) -> None:
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
        self.base_recipe_id: str = base_recipe_id

        self.recipes: List[SmeltingRecipe] = [
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

    def register(self, ctx: TSContext) -> None:
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
        template: IngredientType,
        base: IngredientType,
        addition: IngredientType,
        result: ResultType,
        recipe_id: str = "",
        result_count: int = 1,
    ) -> None:
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
        self.template: IngredientType = template
        self.base: IngredientType = base
        self.addition: IngredientType = addition

    def _to_json(self) -> Dict[str, Any]:
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
        ingredient: IngredientType,
        result: ResultType,
        recipe_id: str = "",
        result_count: int = 1,
    ) -> None:
        """Initialize a cutting board recipe.

        Args:
            ingredient: The input item
            result: The output item
            recipe_id: Unique identifier for this recipe (auto-generated if empty)
            result_count: Number of items to produce
        """
        self.recipe_id: str = recipe_id
        self.ingredient: IngredientType = ingredient
        self.result: ResultType = result
        self.result_count: int = result_count

    def register(self, ctx: TSContext) -> None:
        """Register this cutting board recipe.

        Args:
            ctx: The Tasty Supplies context
        """
        recipe_path: str = f"tasty_supplies:cutting_board/recipes/{self.recipe_id}"
        result_json: Dict[str, Any] = _process_result(
            self.result, count=self.result_count
        )

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
