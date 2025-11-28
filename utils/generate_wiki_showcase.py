from os import listdir
from os.path import isfile, join, abspath
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ⚙️ Config
ITEM_TEXTURES_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/item"
BASE_TEMPLATE = """
{{{{#invoke:Inventory_grid|show
 |items={}
}}}}
"""

FAMILIES = {
    "Pies": ["Pie", "Pie Slice"],
    "Skewers": ["Skewer"],
    "Tools": ["Cleaver", "Knife"],
    "Drinks": ["Cider", "Juice", "Cocoa", "Horn"],
    "Meals": ["Stew", "Salad", "Potato", "Roll", "Rice"],
    "Baked": ["Cookie", "Cake", "Croissant"],
    "Misc": []  # fallback
}

def detect_family(name: str):
    """Retourne la famille correspondant à un item."""
    lname = name.lower()
    for family, keywords in FAMILIES.items():
        for kw in keywords:
            if kw.lower() in lname:
                return family
    return "Misc"

def sort_within_family(items, model):
    """Trie les items d’une famille par similarité sémantique."""
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

    print(f"Found {len(all_names)} items. Generating showcase...")

    # Initialiser le modèle
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    # Regrouper par famille
    family_groups = {}
    for name in all_names:
        fam = detect_family(name)
        family_groups.setdefault(fam, []).append(name)

    # Trier chaque famille par similarité interne
    ordered_items = []
    for fam in FAMILIES.keys():
        if fam not in family_groups:
            continue
        sorted_items = sort_within_family(family_groups[fam], model)
        ordered_items.extend(sorted_items)
        ordered_items.append("")  # slot vide pour séparer les familles

    # Générer le template final
    showcase_template = BASE_TEMPLATE.format(";".join(ordered_items))
    print(showcase_template)

if __name__ == "__main__":
    main()
