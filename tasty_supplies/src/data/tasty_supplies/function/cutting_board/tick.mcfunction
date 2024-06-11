# If a cutting board is placed
execute as @e[type=minecraft:armor_stand] if data entity @s {Tags:["cutting_board_placer"], Rotation:[135.0f, 0.0f]} run data modify entity @s Rotation set value [180.0f, 0.0f]
execute as @e[type=minecraft:armor_stand] if data entity @s {Tags:["cutting_board_placer"], Rotation:[-135.0f, 0.0f]} run data modify entity @s Rotation set value [-180.0f, 0.0f]
execute as @e[type=minecraft:armor_stand] if data entity @s {Tags:["cutting_board_placer"], Rotation:[45.0f, 0.0f]} run data modify entity @s Rotation set value [90.0f, 0.0f]
execute as @e[type=minecraft:armor_stand] if data entity @s {Tags:["cutting_board_placer"], Rotation:[-45.0f, 0.0f]} run data modify entity @s Rotation set value [-90.0f, 0.0f]

execute as @e[type=minecraft:armor_stand] if data entity @s {Tags:["cutting_board_placer"]} at @s run function tasty_supplies:cutting_board/place with entity @s

# Cutting board interaction
execute as @e[type=minecraft:interaction] if data entity @s {Tags:["cutting_board_interaction"]} at @s if data entity @s attack.player on attacker run function tasty_supplies:cutting_board/attack
execute as @e[type=minecraft:interaction] if data entity @s {Tags:["cutting_board_interaction"]} if data entity @s interaction.player run function tasty_supplies:cutting_board/interact with entity @s interaction