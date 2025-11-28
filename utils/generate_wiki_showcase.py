from os import listdir
from os.path import isfile, join, abspath
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ITEM_TEXTURES_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/item"
BASE_TEMPLATE = """
{{{{#invoke:Inventory_grid|show
 |items={}
}}}}
"""

EXCLUDED_TEXTURES = ["Fisherman", "Farmer", "Butcher"]
UNUSED_TEXTURES = ["Ham"]

FAMILIES = {
    "Sweets": ["Pie", "Pie Slice", "Cookie", "Cake", "Croissant", "Honey", "Ice Cream", "Popsicle"],
    "Drinks": ["Cider", "Juice", "Custard", "Cocoa", "Horn", "Gelatin"],
    "Meals": ["Sandwich", "Burger", "Wrap", "Stew", "Skewer", "Salad", "Potato", "Roll", "Rice", "Cheese", "Mutton"],
    "Misc": ["Ice Cream Cone", "Pie Crust"],  # fallback
    "Tools": ["Cleaver", "Knife"],
    "Equipements": ["Hat"]
}

def detect_family(name: str):
    """Returns the family corresponding to an item."""
    lname = name.lower()
    for family, keywords in FAMILIES.items():
        for kw in keywords:
            if kw.lower() in lname:
                return family
    return "Misc"

def sort_within_family(items, model):
    """Sorts items in a family by semantic similarity."""
    if len(items) <= 1:
        return items
    embeddings = model.encode(items, normalize_embeddings=True)
    sims = cosine_similarity(embeddings)
    order = np.argsort(-np.mean(sims, axis=1))
    return [items[i] for i in order]

def main():
    path = abspath(ITEM_TEXTURES_LOCATION)
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    all_names = [f.removesuffix('.png').replace("_", " ").title() for f in all_files]
    
    all_names = [name for name in all_names if name not in EXCLUDED_TEXTURES and name not in UNUSED_TEXTURES]

    print(f"Found {len(all_names)} items. Generating showcase...")

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    family_groups = {}
    for name in all_names:
        fam = detect_family(name)
        family_groups.setdefault(fam, []).append(name)

    showcase_template = ""
    for fam in FAMILIES.keys():
        if fam not in family_groups:
            continue
        sorted_items = sort_within_family(family_groups[fam], model)
        showcase_template += BASE_TEMPLATE.format(";".join(sorted_items))
        
    print(showcase_template)

if __name__ == "__main__":
    main()
