#Mark the ray as having found a block.

scoreboard players set #hit ts_cast_temp 1

#Running custom commands since the block was found.

say Block found.

execute positioned ~ ~ ~ run function tasty_supplies:updater/check/storage