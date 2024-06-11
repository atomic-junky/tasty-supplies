import glob
import io
import math
import json
import requests

from PIL import Image


CRAFTING_TABLE_BG = Image.open("../_media/recipes/blank_recipes/blank_crafting_table_recipe.png").convert("RGBA")
FURNACE_TABLE_BG = Image.open("../_media/recipes/blank_recipes/blank_furnace_recipe.png").convert("RGBA")
CUTTING_BOARD_BG = Image.open("../_media/recipes/blank_recipes/blank_cutting_board_recipe.png").convert("RGBA")
RECIPES_LOCATION = "../../tasty_supplies/src/data/tasty_supplies/recipes/*.json"
ITEMS_LOCATION = "../../tasty_supplies/src/assets/tasty_supplies/textures/item"

MC_TEXTURES_URL = "https://minecraft.wiki/images/Invicon_"

recipes_data = []


def main():    
    _load_recipes_data()
    
    for recipe in recipes_data:
        match _get_recipe_type(recipe):
            case "crafting_shapeless":
                im = _build_crafting_shapeless(recipe)
                im.show()
            case "crafting_shaped":
                # _build_crafting_shaped(recipe)
                pass
            

def _upscale(im, factor):
    return im.resize(tuple(i * factor for i in im.size), Image.Resampling.NEAREST)

def _build_crafting_shapeless(recipe):
    im = _upscale(CRAFTING_TABLE_BG.copy(), 2)
    padding = (58, 32)
    
    ingredients = recipe["ingredients"]
    is_2x2 = len(ingredients) <= 4
    
    index = 0
    for item in ingredients:
        raw = math.floor(index/(2 if is_2x2 else 3))
        col = index - raw*(2 if is_2x2 else 3)
        
        if not item.get("item"):
            texture = _get_item_texture("minecraft:barrier")
        else:
            texture = _get_item_texture(item["item"])
        mask = _create_a_mask(texture)
        
        im.paste(texture, (
            padding[0] + col*(32+2) + col+2,
            padding[1] + raw*(32+2) + raw+2
        ), mask)
        
        index += 1
    
    custom_model_data = _get_custom_model_data(recipe["result"])
    result_texture = _get_item_texture(recipe["result"]["id"], custom_model_data)
    mask = _create_a_mask(result_texture)
    im.paste(texture, (124, 35), mask)
            
    return im.convert("RGBA")


def _get_item_texture(item: str, custom_model_data: int = -1):
    if custom_model_data == -1:
        im = _get_minecraft_texture(item)
    else:
        item_name = item.removeprefix("tasty_supplies:")
        im = Image.open(f"{ITEMS_LOCATION}/{item_name}.png")
    
    im = im.resize((32, 32), Image.Resampling.NEAREST)
    return im


def _get_custom_texture(custom_model_data: int):
    pass


def _get_minecraft_texture(item: str):
    item_name = item.removeprefix("minecraft:")
    item_name = item_name.replace("_", " ")
    item_name = item_name.title()
    item_name = item_name.replace(" ", "_")
    
    url = f"{MC_TEXTURES_URL}{item_name}.png"
    
    res = requests.get(url, stream=True)
    if not res.ok:
        return
    
    im = Image.open(res.raw)
    im = im.convert("RGBA")
    
    return im


def _get_custom_model_data(recipe):
    if recipe.get("components"):
        return recipe["components"]["custom_model_data"]
    
    return -1


def _load_recipes_data():
    paths = glob.glob(RECIPES_LOCATION)
    
    for recipe in paths:
        if recipe.endswith("reversed.json"):
            continue
        
        f = open(recipe)
        data = json.load(f)
        
        recipes_data.append(data)


def _get_recipe_type(recipe):
    return recipe["type"].removeprefix("minecraft:")


def _create_a_mask(im: Image):
    return im.convert('LA')


if __name__ == '__main__':
    main()