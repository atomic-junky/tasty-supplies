## Requirements
## @s => must be a player
## @pos => must be the interaction

# Do nothing if the player is interacting with a knife (or wooden hoe)
execute at @s on target if data entity @s SelectedItem{id:"minecraft:wooden_hoe"} run return run execute as @e[type=interaction, sort=nearest, limit=1] run data remove entity @s interaction

# Do nothing if there is already an item on the cutting board
execute at @s unless data entity @e[type=item_display, distance=..1, limit=1, sort=nearest] item.components."minecraft:custom_data"{tags:["cutting_board_display"]} run return run execute as @e[type=interaction, sort=nearest, limit=1] run data remove entity @s interaction

# Store that the item is custom for later
data modify storage minecraft:temp cutting_board set value {custom_item: false}
execute on target if data entity @s SelectedItem.components run data modify storage minecraft:temp cutting_board set value {custom_item: true}
execute at @s on target run function tasty_supplies:cutting_board/place_item/main with entity @s SelectedItem
data remove entity @s interaction