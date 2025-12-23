execute as @e if data entity @s Inventory run function tasty_supplies:updater/check/inventory/main
# execute as @e if data entity @s Items run function tasty_supplies:updater/check/inventory/main
execute as @e if data entity @s Item run function tasty_supplies:updater/check/item {path:"Item", replace_path:"Item", target:"entity @s"}
execute as @e if data entity @s equipment run function tasty_supplies:updater/check/equipment

scoreboard objectives add ts_cast_temp dummy