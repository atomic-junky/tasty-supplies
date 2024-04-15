kill @s

# If the cutting board is placed in an invalid location
execute align zyx unless block ~ ~ ~ air positioned ~0.5 ~ ~0.5 run return run function tasty_supplies:cutting_board/drop
execute align zyx if block ~ ~-1 ~ air positioned ~0.5 ~ ~0.5 run return run function tasty_supplies:cutting_board/drop

execute align zyx positioned ~0.5 ~0.47 ~0.5 run summon minecraft:item_display ~ ~ ~ {item:{id:"item_frame", count:1, components:{custom_model_data:1, custom_data:{"tags":["cutting_board", "cutting_board_display"]}}}}
execute align zyx run summon minecraft:interaction ~0.5 ~-0.03 ~0.5 {width: 0.875, height: 0.0625, Tags:["cutting_board", "cutting_board_interaction"]}