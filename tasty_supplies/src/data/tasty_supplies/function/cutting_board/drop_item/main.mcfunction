## Requirements
## @pos => must be the interaction

# Make sure there is an item on the cutting board
execute positioned ~ ~0.078125 ~ as @e[type=item_display, distance=..1, limit=1, sort=nearest] if data entity @s item.components."minecraft:custom_data"{tags:["cutting_board_display"]} run return fail

execute positioned ~ ~0.078125 ~ as @e[type=item_display, distance=..1, limit=1, sort=nearest] at @s run function tasty_supplies:cutting_board/drop_item/summon with entity @s
execute positioned ~ ~0.078125 ~ run kill @e[type=item_display, distance=..1, limit=1, sort=nearest]
