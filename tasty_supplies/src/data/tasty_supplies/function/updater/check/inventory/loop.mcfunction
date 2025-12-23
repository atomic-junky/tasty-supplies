data remove storage tasty_supplies:updater SlotsTemp[-1]
data modify storage tasty_supplies:updater SlotsCurrent set from storage tasty_supplies:updater SlotsTemp[-1]

execute if data storage tasty_supplies:updater SlotsTemp[-1] run function tasty_supplies:updater/check/inventory/loop with storage tasty_supplies:updater SlotsTemp[-1]

execute if data storage tasty_supplies:updater SlotsCurrent.components."minecraft:custom_data".ts_hash \
 unless data storage tasty_supplies:updater SlotsCurrent.components{"minecraft:custom_data":{ts_version:"0.14.1"}} run data modify entity @s Inventory append from storage tasty_supplies:updater SlotsCurrent

execute if data storage tasty_supplies:updater SlotsCurrent.components."minecraft:custom_data".hash \
 unless data storage tasty_supplies:updater SlotsCurrent.components{"minecraft:custom_data":{ts_version:"0.14.1"}} run function tasty_supplies:debug_say with storage tasty_supplies:updater SlotsCurrent.components."minecraft:custom_data"

data remove storage tasty_supplies:updater SlotsCurrent