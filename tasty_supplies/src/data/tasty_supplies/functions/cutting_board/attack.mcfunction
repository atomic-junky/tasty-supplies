## Requirements
## @s => must be a player
## @pos => must be the interaction

execute as @e[type=minecraft:interaction, distance=..1, limit=1, sort=nearest] if data entity @s {Tags:["cutting_board_interaction"]} run data remove entity @s attack

# If the cutting board is attacked with a knife
execute if data entity @s SelectedItem{id:"minecraft:wooden_hoe"} if data entity @s SelectedItem.components.minecraft:custom_model_data run return run function tasty_supplies:cutting_board/cut_item

# If the cutting board is attacked with a player's hand
execute unless data entity @s SelectedItem{id:"minecraft:wooden_hoe"} run function tasty_supplies:cutting_board/drop_item/main
