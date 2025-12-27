data modify storage tasty_supplies:updater SlotsCurrent set from storage tasty_supplies:updater SlotsTemp[0]
data remove storage tasty_supplies:updater SlotsTemp[0]

execute store result storage tasty_supplies:updater SlotsLoopIndex int 1 run scoreboard players get @s ts_loop_index
execute store result storage tasty_supplies:updater SlotsCurrentIndex int 1 run data get storage tasty_supplies:updater SlotsCurrent.Slot

execute if data storage tasty_supplies:updater SlotsCurrent.components."minecraft:custom_data".ts_name run function tasty_supplies:updater/check/enderchest/item with storage tasty_supplies:updater

data remove storage tasty_supplies:updater SlotsCurrent
scoreboard players add @s ts_loop_index 1
execute if data storage tasty_supplies:updater SlotsTemp[0] run function tasty_supplies:updater/check/enderchest/loop