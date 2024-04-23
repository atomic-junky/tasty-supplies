## Requirements
## @s => must be a player
## @pos => must be the interaction

execute as @e[type=minecraft:interaction, distance=..1, limit=1, sort=nearest] if data entity @s {Tags:["cutting_board_interaction"]} run data remove entity @s attack

# If the cutting board is attacked with a knife run the cut_item function with the item_display of the cutting board item
execute if data entity @s SelectedItem{id:"minecraft:wooden_hoe"} if data entity @s SelectedItem.components.minecraft:custom_model_data positioned ~ ~0.078125 ~-0.125 as @e[type=item_display, distance=..1, limit=1, sort=nearest] at @s run return run function tasty_supplies:cutting_board/cut_item

# If the cutting board is attacked with a player's hand
# If there's no item break the cutting board
execute positioned ~ ~0.078125 ~ as @e[type=item_display, distance=..1, limit=1, sort=nearest] if data entity @s item.components."minecraft:custom_data"{tags:["cutting_board_display"]} run return run function tasty_supplies:cutting_board/break
# Else drop the item
execute unless data entity @s SelectedItem{id:"minecraft:wooden_hoe"} run function tasty_supplies:cutting_board/drop_item/main
