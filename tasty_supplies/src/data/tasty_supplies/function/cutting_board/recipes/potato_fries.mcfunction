execute if data entity @s item{id: "minecraft:baked_potato", components:{"minecraft:custom_model_data": {"strings": ["baked_potato"]}}} run return fail

summon minecraft:item ~ ~.5 ~ {Item:{id: "minecraft:baked_potato", components:{custom_name: {"text": "Potato Fries", "italic": false},custom_model_data:  {"strings": ["tasty_supplies/potato_fries"]},food: {nutrition: 3.0, saturation: 3.0}}, count: 4}}

kill @s