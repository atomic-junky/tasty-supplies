"""Constants used throughout the Tasty Supplies datapack generator.

This module centralizes all magic strings and constants to improve
maintainability and reduce errors.
"""

# Namespaces
MINECRAFT_NAMESPACE = "minecraft"
TASTY_SUPPLIES_NAMESPACE = "tasty_supplies"

# Prefixes
TAG_PREFIX = "#"
NAMESPACE_SEPARATOR = ":"

# Paths
ITEM_MODEL_PATH = "item"
BLOCK_MODEL_PATH = "block"
FUNCTION_PATH = "function"
RECIPE_PATH = "recipe"

# Default values
DEFAULT_MAX_STACK_SIZE = 64
DEFAULT_BASE_ITEM = "bread"
DEFAULT_COOKING_TIME = 200
DEFAULT_EXPERIENCE = 0.1

# Item model types
MODEL_TYPE_ITEM = "item"
MODEL_TYPE_BLOCK = "block"
MODEL_TYPE_GENERATED = "minecraft:item/generated"
MODEL_TYPE_SELECT = "minecraft:select"
MODEL_TYPE_MODEL = "minecraft:model"

# Recipe types
RECIPE_TYPE_SHAPELESS = "minecraft:crafting_shapeless"
RECIPE_TYPE_SHAPED = "minecraft:crafting_shaped"
RECIPE_TYPE_SMELTING = "minecraft:smelting"
RECIPE_TYPE_BLASTING = "minecraft:blasting"
RECIPE_TYPE_SMOKING = "minecraft:smoking"
RECIPE_TYPE_CAMPFIRE = "minecraft:campfire_cooking"
RECIPE_TYPE_SMITHING = "minecraft:smithing_transform"

# Cooking time multipliers
COOKING_TIME_MULTIPLIER_FAST = 0.5  # For blasting/smoking
COOKING_TIME_MULTIPLIER_SLOW = 3.0  # For campfire

# Recipe categories
RECIPE_CATEGORY_MISC = "misc"
RECIPE_CATEGORY_FOOD = "food"
RECIPE_CATEGORY_BUILDING = "building"
RECIPE_CATEGORY_EQUIPMENT = "equipment"

# Component keys (without namespace)
COMPONENT_CUSTOM_MODEL_DATA = "custom_model_data"
COMPONENT_MAX_STACK_SIZE = "max_stack_size"
COMPONENT_FOOD = "food"
COMPONENT_CONSUMABLE = "consumable"

# Default category name
DEFAULT_CATEGORY = "uncategorized"
