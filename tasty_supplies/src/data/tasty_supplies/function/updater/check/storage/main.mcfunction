scoreboard players set @s ts_loop_index 0
data modify storage tasty_supplies:updater SlotsTemp set from block ~ ~ ~ Items
function tasty_supplies:updater/check/storage/loop with storage tasty_supplies:updater SlotsTemp[0]