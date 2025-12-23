#Setting up the raycasting data.

tag @s add ts_ray
scoreboard players set #hit ts_cast_temp 0
scoreboard players set #distance ts_cast_temp 0

#Running custom pre-raycast commands.

say Before raycasting

#Activating the raycast. This function will call itself until it is done.

function tasty_supplies:updater/find_storage/ray/step

#Running custom post-raycast commands.

say After raycasting

#Raycasting finished, removing tag from the raycaster.

tag @s remove ts_ray