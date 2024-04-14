## Requirements
## @s => a player
## @pos => must be the interaction
## $ => must be an item

# 0.078125 = 1/16 + (1/16)/4
#           1/16 => cutting_board tickness
#           (1/16)/4 => item tickness centered at the middle
# 0.125 = 2/16

execute if data storage minecraft:temp cutting_board{custom_item: true} run function tasty_supplies:cutting_board/place_item/place_custom with entity @s SelectedItem 
$execute unless data storage minecraft:temp cutting_board{custom_item: true} run summon minecraft:item_display ~ ~0.078125 ~-0.125 {item:{id:"$(id)", count:1}, item_display:"ground", Rotation:[0.0f, 90.0f]}

data remove storage minecraft:temp cutting_board.custom_item

$data modify storage minecraft:temp cutting_board.item.id set value "$(id)"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.model_data set from entity @e[type=item_display, sort=nearest, limit=1, distance=..1] item.components."minecraft:custom_model_data"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.food set from entity @e[type=item_display, sort=nearest, limit=1, distance=..1] item.components."minecraft:food"
execute positioned ~ ~0.078125 ~-0.125 run data modify storage minecraft:temp cutting_board.item.name set from entity @e[type=item_display, sort=nearest, limit=1, distance=..1] item.components."minecraft:custom_name"

function tasty_supplies:cutting_board/place_item/remove_player_item with storage minecraft:temp cutting_board.item
