execute if data entity @s equipment.body \
run function tasty_supplies:updater/check/item {data_path:"equipment.body", item_path:"armor.body", target:"entity @s"}

execute if data entity @s equipment.chest \
run function tasty_supplies:updater/check/item {data_path:"equipment.chest", item_path:"armor.chest", target:"entity @s"}

execute if data entity @s equipment.feet \
run function tasty_supplies:updater/check/item {data_path:"equipment.feet", item_path:"armor.feet", target:"entity @s"}

execute if data entity @s equipment.head \
run function tasty_supplies:updater/check/item {data_path:"equipment.head", item_path:"armor.head", target:"entity @s"}

execute if data entity @s equipment.legs \
run function tasty_supplies:updater/check/item {data_path:"equipment.legs", item_path:"armor.legs", target:"entity @s"}

execute if data entity @s equipment.mainhand \
run function tasty_supplies:updater/check/item {data_path:"equipment.mainhand", item_path:"weapon.mainhand", target:"entity @s"}
execute if data entity @s SelectedItem \
run function tasty_supplies:updater/check/item {data_path:"SelectedItem", item_path:"weapon.mainhand", target:"entity @s"}

execute if data entity @s equipment.offhand \
run function tasty_supplies:updater/check/item {data_path:"equipment.offhand", item_path:"weapon.offhand", target:"entity @s"}

execute if data entity @s equipment.saddle \
run function tasty_supplies:updater/check/item {data_path:"equipment.saddle", item_path:"saddle", target:"entity @s"}