kill @s
execute positioned ~ ~0.47 ~ run summon minecraft:item_display ~ ~ ~ {item:{id:"item_frame", count:1, components:{custom_model_data:1, custom_data:{"tags":["cutting_board", "cutting_board_display"]}}}}
summon minecraft:interaction ~ ~-0.03 ~ {width: 0.875, height: 0.0625, Tags:["cutting_board", "cutting_board_interaction"]}