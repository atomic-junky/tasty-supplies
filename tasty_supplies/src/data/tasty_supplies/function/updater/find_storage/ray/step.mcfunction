execute if data block ~ ~ ~ Items run function tasty_supplies:updater/find_storage/ray/hit
scoreboard players add #distance ts_cast_temp 1

execute if score #hit ts_cast_temp matches 0 if score #distance ts_cast_temp matches 251.. run function tasty_supplies:updater/find_storage/ray/failed
execute if score #hit ts_cast_temp matches 0 if score #distance ts_cast_temp matches ..250 positioned ^ ^ ^0.1 run function tasty_supplies:updater/find_storage/ray/step