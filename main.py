from recipe_processor import RecipeProcessor
from recipe_repository import RecipeRepository
import asyncio


async def main():
    repository = RecipeRepository()
    processor = RecipeProcessor(repository)
    await processor.run()


if __name__ == "__main__":
    asyncio.run(main())
