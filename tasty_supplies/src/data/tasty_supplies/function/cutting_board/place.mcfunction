kill @s

# If the cutting board is placed in an invalid location
execute align zyx unless block ~ ~ ~ air positioned ~0.5 ~ ~0.5 run return run function tasty_supplies:cutting_board/drop
execute align zyx if block ~ ~-1 ~ air positioned ~0.5 ~ ~0.5 run return run function tasty_supplies:cutting_board/drop
execute align zyx as @e[type=item_display, distance=..0.5, limit=1] positioned ~0.5 ~ ~0.5 run return run function tasty_supplies:cutting_board/drop

$execute align zyx run summon minecraft:interaction ~0.5 ~ ~0.5 {width: 0.875, height: 0.0625, Tags:["cutting_board", "cutting_board_interaction"], Rotation: $(Rotation)}
$execute align zyx positioned ~0.5 ~0.5 ~0.5 run summon minecraft:item_display ~ ~ ~ {item:{id:"armor_stand", count: 2750014, components:{custom_model_data: {"strings": ["tasty_supplies/cutting_board"]}, custom_data:{"tags":["cutting_board", "cutting_board_display"]}}}, Rotation: $(Rotation), transformation:{left_rotation:{angle:1.57f,axis:[1f,0f,0f]},right_rotation:{angle:1.57f,axis:[0f,0f,1f]},translation:[0f,-0.47f,0f],scale:[1f,1f,1f]}}
