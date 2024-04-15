execute at @s positioned ~ ~0.5 ~ as @e[type=minecraft:item_display, sort=nearest, limit=1, distance=..1] run kill @s
execute at @s positioned ~ ~ ~ as @e[type=minecraft:interaction, sort=nearest, limit=1, distance=..1] run kill @s

summon minecraft:item ~ ~.5 ~ {Item:{id: "minecraft:item_frame", components:{custom_name: "{\"text\": \"Cutting Board\", \"italic\": false}", custom_data: {tags:["cutting_board_placer"]}, entity_data: {id: "minecraft:item_frame", Tags: ["cutting_board_placer"]},custom_model_data: 2750014}}}
