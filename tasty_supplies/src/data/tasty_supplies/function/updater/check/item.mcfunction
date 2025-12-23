$execute unless data entity @s $(path).components."minecraft:custom_data".ts_hash run return fail

$data modify storage tasty_supplies:updater hash set from entity @s $(path).components."minecraft:custom_data".ts_hash
say SHA-1 to check
execute unless function tasty_supplies:updater/check_sha1 run return fail

$data modify storage tasty_supplies:updater item_name set from entity @s $(path).components."minecraft:custom_data".ts_name
$data modify storage tasty_supplies:updater temp.target set from entity @s $(target)
$data modify storage tasty_supplies:updater temp.path set from entity @s $(replace_path)
$data modify storage tasty_supplies:updater temp.count set from entity @s $(path).Count
function tasty_supplies:updater/replace_item with storage tasty_supplies:updater temp