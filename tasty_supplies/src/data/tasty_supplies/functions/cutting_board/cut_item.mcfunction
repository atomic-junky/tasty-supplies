execute if data entity @s item.components."minecraft:custom_data"{tags:["cutting_board_display"]} run return 0

execute if data entity @s item{id: "minecraft:pumpkin_pie", components: {"minecraft:custom_model_data": 2750003}} run function tasty_supplies:cutting_board/recipes/apple_pie_slice
execute if data entity @s item{id: "minecraft:pumpkin_pie", components: {"minecraft:custom_model_data": 2750004}} run function tasty_supplies:cutting_board/recipes/sweet_berry_cheesecake_slice
execute if data entity @s item{id: "minecraft:pumpkin_pie", components: {"minecraft:custom_model_data": 2750005}} run function tasty_supplies:cutting_board/recipes/chocolate_pie_slice
execute if data entity @s item{id: "minecraft:pumpkin_pie", components: {"minecraft:custom_model_data": 2750014}} run function tasty_supplies:cutting_board/recipes/glow_berry_pie_slice
