scoreboard players set @s ts_loop_index 0
data modify storage tasty_supplies:updater SlotsTemp set from entity @s Inventory
function tasty_supplies:updater/check/inventory/loop with storage tasty_supplies:updater SlotsTemp[0]