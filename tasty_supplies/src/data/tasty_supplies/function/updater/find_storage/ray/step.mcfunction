#Running custom per-step commands.

say Raycasting step

#Run a function if a block was successfully detected.

execute if data block ~ ~ ~ Items run function tasty_supplies:updater/find_storage/ray/hit
scoreboard players add #distance ts_cast_temp 1

#If the raycast failed, run a function with the custom commands.

execute if score #hit ts_cast_temp matches 0 if score #distance ts_cast_temp matches 251.. run function tasty_supplies:updater/find_storage/ray/failed
#Advance forward and run the ray again if no entity and/or block was found.

execute if score #hit ts_cast_temp matches 0 if score #distance ts_cast_temp matches ..250 positioned ^ ^ ^0.1 run function tasty_supplies:updater/find_storage/ray/step