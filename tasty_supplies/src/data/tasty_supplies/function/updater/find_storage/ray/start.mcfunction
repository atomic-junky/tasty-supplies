tag @s add ts_ray
scoreboard players set #hit ts_cast_temp 0
scoreboard players set #distance ts_cast_temp 0

function tasty_supplies:updater/find_storage/ray/step

tag @s remove ts_ray