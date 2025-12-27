data modify storage tasty_supplies:updater SlotsCurrent set from storage tasty_supplies:updater SlotsTemp[0]
data remove storage tasty_supplies:updater SlotsTemp[0]

execute store result storage tasty_supplies:updater SlotsLoopIndex int 1 run scoreboard players get @s ts_loop_index
execute store result storage tasty_supplies:updater SlotsCurrentIndex int 1 run data get storage tasty_supplies:updater SlotsCurrent.Slot
execute store result score @s ts_operation_temp run data get storage tasty_supplies:updater SlotsCurrent.Slot
scoreboard players remove @s ts_operation_temp 9

execute if score @s ts_operation_temp matches ..-1 run data modify storage tasty_supplies:updater SlotsName set value "hotbar"
execute if score @s ts_operation_temp matches ..-1 store result storage tasty_supplies:updater SlotsContainerIndex int 1 run data get storage tasty_supplies:updater SlotsCurrentIndex
execute if score @s ts_operation_temp matches 0.. run data modify storage tasty_supplies:updater SlotsName set value "inventory"
execute if score @s ts_operation_temp matches 0.. store result storage tasty_supplies:updater SlotsContainerIndex int 1 run scoreboard players get @s ts_operation_temp

execute if data storage tasty_supplies:updater SlotsCurrent.components."minecraft:custom_data".ts_name run function tasty_supplies:updater/check/inventory/item with storage tasty_supplies:updater

data remove storage tasty_supplies:updater SlotsCurrent
scoreboard players add @s ts_loop_index 1
execute if data storage tasty_supplies:updater SlotsTemp[0] run function tasty_supplies:updater/check/inventory/loop