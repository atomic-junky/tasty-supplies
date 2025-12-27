scoreboard players set @s ts_loop_index 0
data modify storage tasty_supplies:updater SlotsTemp set from entity @s EnderItems
function tasty_supplies:updater/check/enderchest/loop with storage tasty_supplies:updater SlotsTemp[0]