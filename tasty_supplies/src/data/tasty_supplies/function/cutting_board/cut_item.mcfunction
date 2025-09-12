execute if data entity @s item.components."minecraft:custom_data"{tags:["cutting_board_display"]} run return 0

execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/apple_pie"]}}} run function tasty_supplies:cutting_board/recipes/apple_pie_slice
execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/sweet_berry_cheesecake"]}}} run function tasty_supplies:cutting_board/recipes/sweet_berry_cheesecake_slice
execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/chocolate_pie"]}}} run function tasty_supplies:cutting_board/recipes/chocolate_pie_slice
execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/glow_berry_pie"]}}} run function tasty_supplies:cutting_board/recipes/glow_berry_pie_slice
execute if data entity @s item{id: "minecraft:bread", components: {"minecraft:custom_model_data": {"strings": ["tasty_supplies/cheese"]}}} run function tasty_supplies:cutting_board/recipes/cheese_slice
execute if data entity @s item{id: "minecraft:baked_potato"} run function tasty_supplies:cutting_board/recipes/potato_fries
