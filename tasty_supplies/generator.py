from core import *


def generate(ctx: TSContext):
    bucket = Bucket()

    categories = [
        Beverage(bucket),
        Ingredients(bucket),
        Meals(bucket),
        Sweets(bucket),
        Tools(bucket),
        Worksation(bucket),
    ]

    for category in categories:
        category.create_items()

    for category in categories:
        category.create_recipes()

    bucket.register_all(ctx)

    # Generate cutting board drop function
    cutting_board = bucket.get("cutting_board")
    if cutting_board:
        from beet import Function

        ctx.data["tasty_supplies:cutting_board/drop"] = Function(
            [f"summon minecraft:item ~ ~.5 ~ {{Item:{cutting_board.to_result()}}}"]
        )

    item_count = len(bucket.export_item_names())
    recipe_count = len(bucket.export_recipe_ids())

    log.info(f"Items generated")
    log.info(f"\t- {item_count} items")
    log.info(f"\t- {recipe_count} recipes")
