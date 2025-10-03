from core import *


def generate(ctx: TSContext):
    log.info("Generating items...")

    DrinkCategory().register(ctx)
    MealCategory().register(ctx)
    KnifeCategory().register(ctx)
    WorksationCategory().register(ctx)
    Sweets().register(ctx)

    ctx._create_item_showcase()

    log.info(f"Items generated")
    log.info(f"\t- {len(ctx.data.recipes)} recipes")
