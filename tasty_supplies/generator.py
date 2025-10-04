from core import *


def generate(ctx: TSContext):
    log.info("Generating items...")

    Beverage().register(ctx)
    Meals().register(ctx)
    Tools().register(ctx)
    Worksation().register(ctx)
    Sweets().register(ctx)

    log.info(f"Items generated")
    log.info(f"\t- {len(ctx.data.recipes)} recipes")
