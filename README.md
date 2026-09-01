![Tasty Supplies Banner](./docs/_media/tasty_supplies_title.png)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y7DH7YN)

Tasty Supplies is a datapack that add a lot of new foods, recipes and even cooking mechanics in Minecraft by remaining Vanilla.
You'll be able to prepare a wide variety of delicious dishes from cookies to salad and pies.

*For now, the datapack is in early development and there are still many features and recipes to be added. To keep track of what's new and to keep an eye on the progress of the project, you can star the project on [GitHub]([https://github.com/atomic-junky/tasty-supplies](https://github.com/atomic-junky/tasty-supplies)).*

## Features

For now, Tasty Supplies add **+100 recipes**, **2 sets of tools**, **2 equipements** and **1 workstation**.<br>
To know more about it, we invite you to read the [documentation](https://atomic-junky.github.io/tasty-supplies/#/).

<p align="center">
  <img alt="Showcase" src="https://cdn.modrinth.com/data/cached_images/7cb41f96f11dc46a961166225d8ed5d457341d24.png">
</p>

*Some of these textures come from the [Farmer's Delight](https://modrinth.com/mod/farmers-delight) mod*

## Contribute

First, please vote for this [sugestion](https://feedback.minecraft.net/hc/en-us/community/posts/24834246348173-Add-the-new-components-to-crafting-recipe-inputs-Datapacks)! If Mojang add data-driven items, it'll add a bunch of new posibilities for this datapack and many other!

To contribute you'll need to use [beet](https://github.com/mcbeet/beet/tree/728859b2bf7b7725fcf7aa7de3788c668ffd668d).

First link beet to your dev world

```cmd
C:\> beet link <dev_world_name>
```

And second make beet watch all changes

```cmd
C:\> beet watch
```

Replace `beet` with `beet -p ./tasty_supplies/` if you want to stay in the root folder, else do `cd ./tasty_supplies/`.

The build renders block models for the recipe book, which needs OpenGL. On
Linux that means `freeglut3-dev libgl1 libglu1-mesa`, and a display: run the
build under `xvfb-run -a` if you have none.

Like that if you make any changes for the data pack just type `/reload` in minecraft and if you make in any chnages for the resource pack, disable and re-enable the resource pack.

## How it works

This project uses [beet](https://github.com/mcbeet/beet) to generate the data pack
and the resource pack. Instead of writing JSON by hand, you declare items and
recipes in Python: one class per item, in its own file.

```python
# tasty_supplies/ts/catalog/sweets/croissant.py
from ts import Item, food, shaped

from ..ingredients.butter import Butter


@food(6, 3.4)
@shaped(["WBS", "WBS"], W="wheat", B=Butter, S="sugar")
class Croissant(Item):
    pass
```

That is all it takes. The build derives the item id from the class name and
generates the model, the item definition, the recipe, a `give` function, the
page in the in-game cookbook, and the entry letting the pack update the item in
existing worlds. The only thing left to do is to drop
`src/assets/tasty_supplies/textures/item/croissant.png` next to it; the build
warns when a texture is missing.

### Layout

| Path | What lives there |
|---|---|
| `tasty_supplies/ts/catalog/` | the content: one package per category, one module per item |
| `tasty_supplies/ts/declare.py` | every decorator: `@food`, `@apply_effect`, `@shaped`, `@cut`... |
| `tasty_supplies/ts/components.py` | how declarations turn into item components |
| `tasty_supplies/ts/bases.py` | the vanilla items custom items are built on, and why |
| `tasty_supplies/ts/plugins.py` | the steps of the build, listed in `beet.yml` |
| `tasty_supplies/src/` | static data and assets: functions, tags, advancements, textures |

### Conventions

- **Decorators add, the class body configures.** Anything additive -- a
  component, a recipe and its `count` -- is a decorator; the class body only
  fills in the slots an abstract family declares.
- **Families factor out repetition.** `Knife`, `Pie` or `Drink` carry what their
  members share, so an item only states what makes it different.
- **`@component` is the escape hatch.** It covers every vanilla component, and
  every sugar decorator forwards extra keyword arguments to it, so being precise
  never means giving up on the shorthand.
- **A recipe without a new item** is a class of its own:

  ```python
  @shapeless(WheatDough, "wheat", count=2)
  class DoughToBread(Recipe):
      result = "bread"
  ```

- **JSON files in `src/` can read the catalog** through Jinja, which beet runs
  over advancements and loot tables:

  ```jsonc
  "icon": {{ items.iron_cleaver.icon|tojson }}
  ```

  ```jinja
  {{ extend_loot_table("minecraft:entities/squid", pools=[
    {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [items.tentacle.entry()]}
  ]) }}
  ```

### Checks

The build fails on the mistakes that used to slip through: an item whose
support is shared with another one, or generic enough that a vanilla item would
satisfy the recipe. `ts/registry.py` lists the ones that are known and still
waiting to be fixed.

## Credits

Certain item textures/models come from or are based on [Farmer's Delight](https://github.com/vectorwing/FarmersDelight) and [Nether's Delight](https://github.com/Chefs-Delight/NethersDelight_Forge).
