"""Bucket class for gathering and managing custom items and recipes.

The Bucket class collects all custom items and recipes, storing them
for easy reference and usage across the generation system. It provides methods to
register items and recipes, retrieve them by name or category, and manage
the generation pipeline.
"""

from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable

from .models.item import Item
from .models.context import TSContext
from .logger import log


@runtime_checkable
class RecipeProtocol(Protocol):
    """Protocol for recipes that have a recipe_id attribute."""

    recipe_id: str

    def register(self, ctx: TSContext) -> None: ...


@runtime_checkable
class AutoCookingRecipeProtocol(Protocol):
    """Protocol for AutoCookingRecipe which contains multiple recipes."""

    recipes: List[RecipeProtocol]


@runtime_checkable
class AdvancementProtocol(Protocol):
    """Protocol for advancement-like objects."""

    advancement_id: str

    def register(self, ctx: TSContext) -> None: ...


RecipeType = Union[RecipeProtocol, AutoCookingRecipeProtocol]
AdvancementType = AdvancementProtocol


class Bucket:
    """A container for managing custom items, recipes, and their metadata.

    This class acts as a registry for all custom items and recipes created during generation.
    Items and recipes are managed separately, while recipes define crafting relationships.

    Attributes:
        _items (Dict[str, Item]): Dictionary mapping item names to Item objects.
        _recipes (List[RecipeProtocol]): List of recipe objects to be registered.
        _item_categories (Dict[str, List[str]]): Dictionary mapping category names to item lists.
        _recipe_categories (Dict[str, List[str]]): Dictionary mapping categories to recipe IDs.
    """

    def __init__(self) -> None:
        """Initialize an empty Bucket."""
        self._items: Dict[str, Item] = {}
        self._recipes: List[RecipeProtocol] = []
        self._advancements: List[AdvancementType] = []
        self._item_categories: Dict[str, List[str]] = {}
        self._recipe_categories: Dict[str, List[str]] = {}
        self._advancement_categories: Dict[str, List[str]] = {}
        self._recipe_id_counter: Dict[str, int] = {}  # Track recipe_id usage

    def add_item(self, item: Item, category: Optional[str] = None) -> None:
        """Add an item to the bucket.

        Args:
            item: The Item object to add.
            category: Category name to organize items (optional).
        """
        if item.name in self._items:
            log.warning(
                f"Item '{item.name}' already exists in bucket. Skipping duplicate."
            )
            return

        self._items[item.name] = item

        # Store in category
        category_key = category or "uncategorized"
        if category_key not in self._item_categories:
            self._item_categories[category_key] = []
        self._item_categories[category_key].append(item.name)

        log.debug(f"Added item '{item.name}' to bucket in category '{category_key}'.")

    def _generate_recipe_id(self, recipe: RecipeProtocol) -> str:
        """Generate a unique recipe_id for a recipe.

        If the recipe already has a recipe_id, returns it.
        Otherwise, generates one based on the result item name.

        Args:
            recipe: The recipe object

        Returns:
            A unique recipe_id string
        """
        # If recipe already has a non-empty recipe_id, use it
        if hasattr(recipe, "recipe_id") and recipe.recipe_id:
            return recipe.recipe_id

        # Try to extract base name from result
        base_name: str = "recipe"
        if hasattr(recipe, "result"):
            result: Any = recipe.result
            if isinstance(result, Item):
                base_name = result.name
            elif isinstance(result, dict) and "id" in result:
                # Extract item name from dict result
                item_id: str = result["id"]
                if ":" in item_id:
                    base_name = item_id.split(":")[1]
                else:
                    base_name = item_id
            elif isinstance(result, str):
                base_name = result.split(":")[-1]

        # Ensure uniqueness by adding a counter if needed
        if base_name not in self._recipe_id_counter:
            self._recipe_id_counter[base_name] = 0
            return base_name
        else:
            self._recipe_id_counter[base_name] += 1
            return f"{base_name}_{self._recipe_id_counter[base_name]}"

    def add_recipe(self, recipe: RecipeType, category: Optional[str] = None) -> None:
        """Add a recipe to the bucket.

        Automatically generates a recipe_id if the recipe doesn't have one or if it's empty.

        Args:
            recipe: The recipe object to add (can be a single recipe or AutoCookingRecipe).
            category: Category name to organize recipes (optional).
        """
        # Handle AutoCookingRecipe which contains multiple recipes
        if hasattr(recipe, "recipes") and isinstance(recipe.recipes, list):
            # This is an AutoCookingRecipe
            # If base_recipe_id is empty, generate one from the first sub-recipe
            base_id: str = ""
            if hasattr(recipe, "base_recipe_id"):
                base_id = recipe.base_recipe_id

            if not base_id:
                # Generate base ID from the first sub-recipe's result
                base_id = self._generate_recipe_id(recipe.recipes[0])

            # Now assign IDs to each sub-recipe with appropriate suffixes
            suffixes: List[str] = ["blasting", "smoking", "campfire"]
            for i, sub_recipe in enumerate(recipe.recipes):
                # Generate recipe_id if needed
                if not hasattr(sub_recipe, "recipe_id") or not sub_recipe.recipe_id:
                    sub_recipe.recipe_id = f"{base_id}_{suffixes[i]}"

                self._recipes.append(sub_recipe)
                if category:
                    if category not in self._recipe_categories:
                        self._recipe_categories[category] = []
                    self._recipe_categories[category].append(sub_recipe.recipe_id)
                log.debug(
                    f"Added recipe '{sub_recipe.recipe_id}' to bucket (from AutoCookingRecipe)."
                )
        else:
            # This is a regular recipe
            # Generate recipe_id if needed
            if not hasattr(recipe, "recipe_id") or not recipe.recipe_id:
                recipe.recipe_id = self._generate_recipe_id(recipe)

            self._recipes.append(recipe)

            # Store in category
            if category:
                if category not in self._recipe_categories:
                    self._recipe_categories[category] = []
                self._recipe_categories[category].append(recipe.recipe_id)

            log.debug(f"Added recipe '{recipe.recipe_id}' to bucket.")

    def add_advancement(self, advancement: AdvancementType, category: Optional[str] = None) -> None:
        """Add an advancement to the bucket.

        Args:
            advancement: The advancement object to add.
            category: Optional category label used for reporting.
        """

        # Avoid duplicates by id
        existing_ids = {adv.advancement_id for adv in self._advancements}
        if advancement.advancement_id in existing_ids:
            log.warning(
                f"Advancement '{advancement.advancement_id}' already registered in bucket. Skipping duplicate."
            )
            return

        self._advancements.append(advancement)

        if category:
            if category not in self._advancement_categories:
                self._advancement_categories[category] = []
            self._advancement_categories[category].append(advancement.advancement_id)

        log.debug(f"Added advancement '{advancement.advancement_id}' to bucket.")

    def get(self, item_name: str) -> Optional[Item]:
        """Retrieve an item by name.

        Args:
            item_name (str): The name of the item to retrieve.

        Returns:
            Item or None: The Item object if found, None otherwise.
        """
        return self._items.get(item_name)

    def get_ingredient(self, item_name: str) -> Optional[str]:
        """Retrieve the base_item (Minecraft item ID) of an item by name.

        This is useful for recipes that need the base Minecraft item
        rather than the full Item object. Returns the base_item which can
        be used directly in recipe ingredients.

        Args:
            item_name (str): The name of the item to retrieve.

        Returns:
            str or None: The base_item ID if found, None otherwise.

        Example:
            >>> bucket.get_ingredient("butter")  # Returns "poisonous_potato"
        """
        item = self._items.get(item_name)
        return item.base_item if item else None

    def get_all(self) -> Dict[str, Item]:
        """Get all items in the bucket.

        Returns:
            Dict[str, Item]: Dictionary of all items mapped by name.
        """
        return self._items.copy()

    def get_items_by_category(self, category: str) -> List[str]:
        """Get all item names in a specific category.

        Args:
            category: The category name.

        Returns:
            List of item names in the category, or empty list if not found.
        """
        return self._item_categories.get(category, []).copy()

    def get_recipes_by_category(self, category: str) -> List[str]:
        """Get all recipe IDs in a specific category.

        Args:
            category: The category name.

        Returns:
            List of recipe IDs in the category, or empty list if not found.
        """
        return self._recipe_categories.get(category, []).copy()

    def get_item_categories(self) -> List[str]:
        """Get all item category names.

        Returns:
            List of all item category names.
        """
        return list(self._item_categories.keys())

    def get_recipe_categories(self) -> List[str]:
        """Get all recipe category names.

        Returns:
            List of all recipe category names.
        """
        return list(self._recipe_categories.keys())

    def get_advancements_by_category(self, category: str) -> List[str]:
        """Get all advancement IDs in a specific category.

        Args:
            category: The category name.

        Returns:
            List of advancement IDs in the category, or empty list if not found.
        """

        return self._advancement_categories.get(category, []).copy()

    def contains_item(self, item_name: str) -> bool:
        """Check if an item exists in the bucket.

        Args:
            item_name: The name of the item.

        Returns:
            True if the item exists, False otherwise.
        """
        return item_name in self._items

    def item_count(self) -> int:
        """Get the total number of items in the bucket.

        Returns:
            Total count of items.
        """
        return len(self._items)

    def recipe_count(self) -> int:
        """Get the total number of recipes in the bucket.

        Returns:
            Total count of recipes.
        """
        return len(self._recipes)

    def advancement_count(self) -> int:
        """Get the total number of advancements in the bucket."""

        return len(self._advancements)

    def register_all(self, ctx: TSContext) -> None:
        """Register all items and recipes with the given context.

        This method registers all collected items and recipes with the context,
        making them available in the build process. Items are registered first,
        then recipes, then give commands.

        Args:
            ctx: The Beet context to register with.
        """
        # Register all items first
        for item_name, item in self._items.items():
            item.register(ctx)
            log.debug(f"Registered item '{item_name}' with context.")

        # Then register all recipes
        for recipe in self._recipes:
            recipe.register(ctx)

        # Then register all advancements
        for advancement in self._advancements:
            advancement.register(ctx)

        # Finally generate give commands for all items
        self._generate_give_commands(ctx)

    def _generate_give_commands(self, ctx: TSContext) -> None:
        """Generate /give commands for all custom items.

        Creates a function file for each item at function/give/{item_name}.mcfunction
        that gives the player that item with all its custom properties.

        Args:
            ctx: The Tasty Supplies context
        """
        from beet import Function

        def remove_minecraft_namespace(data: Any) -> Any:
            """Remove 'minecraft:' prefix from component keys.

            Args:
                data: The data structure to process (dict, list, or primitive)

            Returns:
                Data with minecraft namespace removed from keys
            """
            if isinstance(data, dict):
                return {
                    key.replace("minecraft:", ""): remove_minecraft_namespace(value)
                    for key, value in data.items()
                }
            elif isinstance(data, list):
                return [remove_minecraft_namespace(item) for item in data]
            else:
                return data

        def to_snbt(data: Any) -> str:
            """Convert Python data to SNBT (Stringified NBT) format for Minecraft commands.

            Args:
                data: The data to convert (dict, list, string, bool, number)

            Returns:
                SNBT formatted string
            """
            if isinstance(data, dict):
                items: List[str] = [
                    f"{key}:{to_snbt(value)}" for key, value in data.items()
                ]
                return "{" + ",".join(items) + "}"
            elif isinstance(data, list):
                items: List[str] = [to_snbt(item) for item in data]
                return "[" + ",".join(items) + "]"
            elif isinstance(data, str):
                # Escape quotes in strings
                return '"' + data.replace('"', '\\"') + '"'
            elif isinstance(data, bool):
                return "true" if data else "false"
            elif isinstance(data, (int, float)):
                return str(data)
            else:
                return str(data)

        for item_name, item in self._items.items():
            item_data: Dict[str, Any] = item.to_result()
            base_item: str = item_data["id"]
            count: int = item_data.get("count", 1)
            components: Dict[str, Any] = item_data.get("components", {})
            components = remove_minecraft_namespace(components)

            # Generate SNBT for components
            snbt_components: str
            if components:
                component_items: List[str] = [
                    f"{key}={to_snbt(value)}" for key, value in components.items()
                ]
                snbt_components = ",".join(component_items)
            else:
                snbt_components = ""

            give_command: str = f"give @s {base_item}[{snbt_components}] {count}"

            ctx.data["tasty_supplies"].functions[f"give/{item_name}"] = Function(
                [give_command]
            )
            log.debug(f"Generated give command for '{item_name}'")

    def export_item_names(self) -> List[str]:
        """Export all item names as a list.

        Returns:
            List of all item names in the bucket.
        """
        return list(self._items.keys())

    def export_recipe_ids(self) -> List[str]:
        """Export all recipe IDs as a list.

        Returns:
            List of all recipe IDs in the bucket.
        """
        return [r.recipe_id for r in self._recipes]

    def export_advancement_ids(self) -> List[str]:
        """Export all advancement IDs as a list."""

        return [a.advancement_id for a in self._advancements]

    def export_by_base_item(self) -> Dict[str, List[str]]:
        """Export items grouped by their base item.

        Returns:
            Dict[str, List[str]]: Dictionary mapping base item names to lists of custom items using that base.
        """
        by_base: Dict[str, List[str]] = {}
        for item_name, item in self._items.items():
            base: str = item.base_item
            if base not in by_base:
                by_base[base] = []
            by_base[base].append(item_name)
        return by_base

    def export_summary(self) -> Dict[str, Any]:
        """Export a summary of all items, recipes, and categories in the bucket.

        Returns:
            Dict with summary data including counts and categorizations.
        """
        return {
            "total_items": self.item_count(),
            "total_recipes": self.recipe_count(),
            "total_advancements": self.advancement_count(),
            "item_categories": {
                category: len(items)
                for category, items in self._item_categories.items()
            },
            "recipe_categories": {
                category: len(recipes)
                for category, recipes in self._recipe_categories.items()
            },
            "advancement_categories": {
                category: len(advancements)
                for category, advancements in self._advancement_categories.items()
            },
            "items_by_category": {
                category: items[:] for category, items in self._item_categories.items()
            },
            "recipes_by_category": {
                category: recipes[:]
                for category, recipes in self._recipe_categories.items()
            },
            "advancements_by_category": {
                category: advancements[:]
                for category, advancements in self._advancement_categories.items()
            },
        }

    def clear(self) -> None:
        """Clear all items and recipes from the bucket."""
        self._items.clear()
        self._recipes.clear()
        self._advancements.clear()
        self._item_categories.clear()
        self._recipe_categories.clear()
        self._advancement_categories.clear()
        log.debug("Bucket cleared.")

    def __repr__(self) -> str:
        """String representation of the Bucket."""
        return (
            f"Bucket(items={self.item_count()}, recipes={self.recipe_count()}, "
            f"advancements={self.advancement_count()}, "
            f"item_categories={len(self._item_categories)}, "
            f"recipe_categories={len(self._recipe_categories)}, "
            f"advancement_categories={len(self._advancement_categories)})"
        )
