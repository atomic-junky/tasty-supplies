# Print the log message before updating the scoreboard to after update the value and return instantly.

execute if score #ts_settings disable_update matches 1.. run tellraw @s "§6§l[Tasty Supplies] §r§7Updater system enabled."
execute if score #ts_settings disable_update matches ..0 run tellraw @s "§6§l[Tasty Supplies] §r§7Updater system disabled."

execute if score #ts_settings disable_update matches ..0 run return run scoreboard players set #ts_settings disable_update 1
execute if score #ts_settings disable_update matches 1.. run return run scoreboard players set #ts_settings disable_update 0
