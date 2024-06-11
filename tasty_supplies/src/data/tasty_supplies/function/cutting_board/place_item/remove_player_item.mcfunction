## Requirements
## @s => a player
## $ => stored item components

execute if data storage minecraft:temp cutting_board.item.model_data run function tasty_supplies:cutting_board/place_item/remove_custom_item with storage minecraft:temp cutting_board.item
$execute unless data storage minecraft:temp cutting_board.item.model_data run clear @s $(id) 1

data remove storage minecraft:temp cutting_board.item