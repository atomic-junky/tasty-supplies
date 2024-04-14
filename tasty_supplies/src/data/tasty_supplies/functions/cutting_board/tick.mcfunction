# If a cutting board is placed
execute as @e[type=minecraft:item_frame] if data entity @s {Tags:["cutting_board_placer"]} at @s run function tasty_supplies:cutting_board/place

# Cutting board interaction
execute as @e[type=minecraft:interaction] if data entity @s {Tags:["cutting_board_interaction"]} at @s if data entity @s attack.player on attacker run function tasty_supplies:cutting_board/attack
execute as @e[type=minecraft:interaction] if data entity @s {Tags:["cutting_board_interaction"]} if data entity @s interaction.player run function tasty_supplies:cutting_board/interact with entity @s interaction