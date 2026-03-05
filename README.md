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

Like that if you make any changes for the data pack just type `/reload` in minecraft and if you make in any chnages for the resource pack, disable and re-enable the resource pack.

## How it works

This project uses [beet](https://github.com/mcbeet/beet) to automatically generate Minecraft datapacks and resource packs. Instead of writing complex JSON files manually, you define items and recipes in Python.

## Credits

Certain items texture/models come from or are base on [Farmer's Delight](https://github.com/vectorwing/FarmersDelight) and [Nether's Delight](https://github.com/Chefs-Delight/NethersDelight_Forge).
