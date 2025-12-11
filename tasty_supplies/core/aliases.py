"""Aliases for custom items that use vanilla Minecraft base items.

This module maps custom item names to their corresponding vanilla
Minecraft item IDs used as base items.
Aliases often use uncommon items so that custom items can be used in recipes without the player being too likely to use the wrong item in the wrong recipe.
That's why pottery sherds, banner patterns, and armor trims are often used as aliases.
Grouping all aliases here makes it easier to see which items are already used as aliases and avoid errors.

Note: Pottery sherds can be more easily used in recipes with the crafting table, which is why it is preferable to use them for ingredients that are not used in the crafting table.
"""

# Food items
BARNACLE_THONG: str = "guster_banner_pattern"
BUTTER: str = "poisonous_potato"
CHEESE_SLICE: str = "piglin_banner_pattern"
COOKED_BACON: str = "skull_banner_pattern"
COOKED_BARNACLE_THONG: str = "creeper_banner_pattern"
COOKED_RICE: str = "field_masoned_banner_pattern"
COOKED_TENTACLE: str = "mojang_banner_pattern"
FRIED_EGG: str = "piglin_banner_pattern"
GLARE_EYE: str = "sentry_armor_trim_smithing_template"
GREAT_HUNGER_TEETH: str = "vex_armor_trim_smithing_template"
GUARDIAN_TAIL: str = "flow_banner_pattern"
PIE_CRUST: str = "angler_pottery_sherd"
RAW_BACON: str = "archer_pottery_sherd"
RAW_COD_SLICE: str = "flower_banner_pattern"
RAW_SALMON_SLICE: str = "bordure_indented_banner_pattern"
RICE: str = "arms_up_pottery_sherd"
TENTACLE: str = "blade_pottery_sherd"

# Tool items
DIAMOND_KNIFE: str = "disc_fragment_5"
DIAMOND_CLEAVER: str = "echo_shard"
