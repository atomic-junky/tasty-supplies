execute at @s positioned ~ ~0.5 ~ as @e[type=minecraft:item_display, sort=nearest, limit=1, distance=..1] run kill @s
execute at @s positioned ~ ~ ~ as @e[type=minecraft:interaction, sort=nearest, limit=1, distance=..1] run kill @s

function tasty_supplies:cutting_board/drop