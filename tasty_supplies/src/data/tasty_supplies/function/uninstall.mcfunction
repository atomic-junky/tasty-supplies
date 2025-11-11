execute as @e[type=minecraft:interaction] if data entity @s {Tags:["cutting_board_interaction"]} run kill @s
execute as @e[type=minecraft:item_display] if data entity @s item.components{"minecraft:custom_data": {tags:["cutting_board"]}} at @s as @e[type=minecraft:item_display, distance=..1] run kill @s
execute as @e[type=minecraft:item_display,tag=ts.crop] run kill @s
scoreboard objectives remove tsc_age
scoreboard objectives remove tsc_max
scoreboard objectives remove tsc_timer
scoreboard objectives remove tsc_int