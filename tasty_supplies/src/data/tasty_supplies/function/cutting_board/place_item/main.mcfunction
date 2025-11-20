## Requirements
## @s => a player
## @pos => must be the interaction
## $ => must be an item

# 0.078125 = 1/16 + (1/16)/4
#           1/16 => cutting_board tickness
#           (1/16)/4 => item tickness centered at the middle
# 0.125 = 2/16

execute if data storage minecraft:temp cutting_board{custom_item: true} run function tasty_supplies:cutting_board/place_item/place_custom with entity @s SelectedItem
$execute unless data storage minecraft:temp cutting_board{custom_item: true} run summon minecraft:item_display ~ ~0.078125 ~ {item:{id:"$(id)", count: 1}, item_display:"ground", Tags:["cutting_board_slice","cutting_board_new"]}

# Rotate and translate the item_display
execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ as @e[type=minecraft:item_display, tag=cutting_board_new, sort=nearest, limit=1] run data modify entity @s transformation.translation[1] set value -0.125f

execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ if data entity @s {Rotation:[0.0f, 0.0f]} as @e[type=minecraft:item_display, sort=nearest, limit=1] run data modify entity @s Rotation set value [180.0f, 90.0f]

execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ if data entity @s {Rotation:[180.0f, 0.0f]} as @e[type=minecraft:item_display, sort=nearest, limit=1] run data modify entity @s Rotation set value [0.0f, 90.0f]
execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ if data entity @s {Rotation:[-180.0f, 0.0f]} as @e[type=minecraft:item_display, sort=nearest, limit=1] run data modify entity @s Rotation set value [0.0f, 90.0f]

execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ if data entity @s {Rotation:[90.0f, 0.0f]} as @e[type=minecraft:item_display, sort=nearest, limit=1] run data modify entity @s Rotation set value [-90.0f, 90.0f]

execute as @e[type=interaction, sort=nearest, limit=1] positioned ~ ~0.078125 ~ if data entity @s {Rotation:[-90.0f, 0.0f]} as @e[type=minecraft:item_display, sort=nearest, limit=1] run data modify entity @s Rotation set value [90.0f, 90.0f]

data remove storage minecraft:temp cutting_board.custom_item

$data modify storage minecraft:temp cutting_board.item.id set value "$(id)"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.model_data set from entity @e[type=item_display, tag=cutting_board_new, sort=nearest, limit=1, distance=..1] item.components."minecraft:custom_model_data"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.food set from entity @e[type=item_display, tag=cutting_board_new, sort=nearest, limit=1, distance=..1] item.components."minecraft:food"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.name set from entity @e[type=item_display, tag=cutting_board_new, sort=nearest, limit=1, distance=..1] item.components."minecraft:custom_name"

function tasty_supplies:cutting_board/place_item/remove_player_item with storage minecraft:temp cutting_board.item
