scoreboard objectives add ts_cast_temp dummy
scoreboard objectives add ts_operation_temp dummy
scoreboard objectives add ts_loop_index dummy

execute as @e if data entity @s Inventory run function tasty_supplies:updater/check/inventory/main
execute as @e if data entity @s EnderItems run function tasty_supplies:updater/check/enderchest/main
execute as @e if data entity @s equipment run function tasty_supplies:updater/check/equipment
