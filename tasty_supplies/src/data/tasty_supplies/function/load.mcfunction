scoreboard objectives add disable_update dummy
execute unless score #ts_settings disable_update matches 1.. run scoreboard players set #ts_settings disable_update 0

function tasty_supplies:events/on_load
execute if score #ts_settings disable_update matches ..0 run function tasty_supplies:updater/on_load

function tasty_supplies:tick_20