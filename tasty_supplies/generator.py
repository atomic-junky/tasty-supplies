from core import *


def generate(ctx: TSContext):
    log.info("Generating items...")

    # Create a bucket to store all items and recipes
    bucket = Bucket()

    # Initialize all categories
    categories = [
        Beverage(bucket),
        Ingredients(bucket),
        Meals(bucket),
        Sweets(bucket),
        Tools(bucket),
        Worksation(bucket),
    ]

    # PHASE 1: Create all items from all categories first
    log.debug("Phase 1: Creating all items...")
    for category in categories:
        category.create_items()

    # PHASE 2: Create all recipes (now all items are available)
    log.debug("Phase 2: Creating all recipes...")
    for category in categories:
        category.create_recipes()

    # Register showcase items and special functions
    for category in categories:
        category.register(ctx)

    # Register all items and recipes from the bucket
    bucket.register_all(ctx)

    log.info(f"Items generated")
    log.info(f"\t- {len(ctx.data.recipes)} recipes")
