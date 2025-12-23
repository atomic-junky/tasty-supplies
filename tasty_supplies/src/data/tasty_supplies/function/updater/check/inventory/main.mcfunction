# data modify storage tasty_supplies:updater Slots set value []
# data modify storage tasty_supplies:updater SlotsTemp set value []

data modify storage tasty_supplies:updater SlotsTemp set from entity @s Inventory

function tasty_supplies:updater/check/inventory/loop with storage tasty_supplies:updater SlotsTemp[-1]