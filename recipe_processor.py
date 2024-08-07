from aiohttp import web
from pretty_log import pretty_log
from recipe_repository import RecipeRepository
from opc_ua_client import OPCUAClient
from config import config
import asyncio


class RecipeProcessor:
    def __init__(self, repository: RecipeRepository):
        self.app = web.Application()
        self.repository = repository
        self.opcua_client = OPCUAClient()
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_post(config["CLIENT_ENTRY_POINT"], self.receive_recipe)

    async def receive_recipe(self, request):
        data = await request.json()
        recipe = data.get("recipe")
        if recipe:
            try:
                self.repository.add_new_items([recipe])
                return web.json_response(
                    {"status": "success", "recipe": recipe}, status=200
                )
            except Exception as e:
                pretty_log(f"ERRO: {repr(e)}")
                return web.json_response(
                    {"status": "error", "message": "Failed to add recipe"}, status=500
                )
        else:
            return web.json_response(
                {"status": "error", "message": "No recipe provided"}, status=400
            )

    async def send_recipe_to_machine(self, recipe_id, recipe):
        try:
            response = await self.opcua_client.config(recipe)
            pretty_log(f"Enviando receita para a máquina: {recipe}")
            return response
        except Exception as e:
            pretty_log(f"ERRO ao enviar receita para a máquina: {repr(e)}")
            return False

    def alert_failure(self, recipe):
        pretty_log(
            f"Failed to send recipe to the machine: {recipe}. An email will be sent notifying about the issue."
        )


    async def process_queue(self):
        while True:
            try:
                self.recipe_queue = self.repository.load_queue()

                while not self.recipe_queue.empty():
                    recipe_id, recipe, retries = self.recipe_queue.get()
                    pretty_log(
                        f"Processing recipe: ID={recipe_id}, Recipe={recipe}, Retries={retries}"
                    )

                    success = await self.send_recipe_to_machine(recipe_id, recipe)

                    if success:
                        self.repository.mark_as_processed(recipe_id)
                        pretty_log(f"Recipe ID={recipe_id} marked as processed")
                    else:
                        self.repository.increment_retries(recipe_id)
                        pretty_log(f"Recipe ID={recipe_id} retries incremented")

                        if (
                            self.repository.get_retries(recipe_id)
                            >= config["MAX_QUEUE_RETRIES"]
                        ):
                            self.alert_failure(recipe)

                self.repository.remove_processed_items()

            except Exception as e:
                pretty_log(f"An error occurred while processing the queue: {e}")

            await asyncio.sleep(5)

    async def run(self):
        await self.opcua_client.start()
        asyncio.create_task(self.process_queue())
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(
            runner, host=config["CLIENT_HOST"], port=config["CLIENT_PORT"]
        )
        await site.start()
        pretty_log(
            "Server started on http://{}:{}".format(
                config["CLIENT_HOST"], config["CLIENT_PORT"]
            )
        )

        while True:
            await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(RecipeProcessor(RecipeRepository()).run())
