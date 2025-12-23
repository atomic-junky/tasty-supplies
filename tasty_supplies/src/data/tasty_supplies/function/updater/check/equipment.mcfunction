execute if data entity @s equipment.body \
 run function tasty_supplies:updater/check/item {path:"equipment.body", replace_path:"equipment.body", target:"entity @s"}

execute if data entity @s equipment.chest \ 
 run function tasty_supplies:updater/check/item {path:"equipment.chest", replace_path:"equipment.chest", target:"entity @s"}

execute if data entity @s equipment.feet \
 run function tasty_supplies:updater/check/item {path:"equipment.feet", replace_path:"equipment.feet", target:"entity @s"}

execute if data entity @s equipment.head \
 run function tasty_supplies:updater/check/item {path:"equipment.head", replace_path:"equipment.head", target:"entity @s"}

execute if data entity @s equipment.legs \
 run function tasty_supplies:updater/check/item {path:"equipment.legs", replace_path:"equipment.legs", target:"entity @s"}

execute if data entity @s equipment.mainhand \
 run function tasty_supplies:updater/check/item {path:"equipment.mainhand", replace_path:"equipment.mainhand", target:"entity @s"}
execute if data entity @s SelectedItem \
 run function tasty_supplies:updater/check/item {path:"SelectedItem", replace_path:"equipment.mainhand", target:"entity @s"}

execute if data entity @s equipment.offhand \
 run function tasty_supplies:updater/check/item {path:"equipment.offhand", replace_path:"equipment.offhand", target:"entity @s"}

execute if data entity @s equipment.saddle \
 run function tasty_supplies:updater/check/item {path:"equipment.saddle", replace_path:"equipment.saddle", target:"entity @s"}