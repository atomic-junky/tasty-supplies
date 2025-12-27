$execute unless data $(target) $(data_path).components."minecraft:custom_data".ts_name run return fail

data remove storage tasty_supplies:updater temp

$execute unless data $(target) $(data_path).components."minecraft:custom_data".ts_hash run \
 data modify storage tasty_supplies:updater temp.hash set value "-1"
$execute if data $(target) $(data_path).components."minecraft:custom_data".ts_hash run \
 data modify storage tasty_supplies:updater temp.hash set from $(target) $(data_path).components."minecraft:custom_data".ts_hash
execute if function tasty_supplies:updater/check_sha1 run return fail

$data modify storage tasty_supplies:updater temp.item_name set from $(target) $(data_path).components."minecraft:custom_data".ts_name
$data modify storage tasty_supplies:updater temp.target set value "$(target)"
$data modify storage tasty_supplies:updater temp.path set value "$(item_path)"
$data modify storage tasty_supplies:updater temp.count set from $(target) $(data_path).count
function tasty_supplies:updater/replace_item with storage tasty_supplies:updater temp