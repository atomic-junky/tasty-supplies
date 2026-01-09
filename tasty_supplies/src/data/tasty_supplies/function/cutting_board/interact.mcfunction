## Requirements
## @s => must be a player
## @pos => must be the interaction

# Do nothing if the player is interacting with a cutting tool
execute at @s on target if data entity @s SelectedItem.components."minecraft:custom_data".ts_cutting_tool run return run execute as @e[type=interaction, sort=nearest, limit=1] run data remove entity @s interaction

# Do nothing if there is already an item on the cutting board
# If an item_display slice exists within reach, remove the interaction and stop.
execute at @s if entity @e[type=item_display, tag=cutting_board_slice, distance=..1] run execute as @e[type=interaction, sort=nearest, limit=1] run data remove entity @s interaction
execute at @s if entity @e[type=item_display, tag=cutting_board_slice, distance=..1] run return fail

# Store that the item is custom for later
data modify storage minecraft:temp cutting_board set value {custom_item: false}
execute on target if data entity @s SelectedItem.components run data modify storage minecraft:temp cutting_board set value {custom_item: true}
execute at @s on target run function tasty_supplies:cutting_board/place_item/main with entity @s SelectedItem
data remove entity @s interaction