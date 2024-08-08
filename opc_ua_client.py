from asyncua import Client as UaClient
from config import config
from pretty_log import pretty_log
import asyncio


class OPCUAClient:
    def __init__(self):
        self.endpoint = config["OPCUA_SERVER_ENDPOINT"]
        self.namespace = "1"
        self.client = None
        self.connected = False

    async def start(self):
        pretty_log(f"Connecting to {self.endpoint} ...")
        try:
            self.client = UaClient(url=self.endpoint)
            await self.client.connect()
            nsidx = await self.client.get_namespace_index(self.namespace)
            pretty_log(f"Namespace Index for '{self.namespace}': {nsidx}")
            self.connected = True

        except ConnectionRefusedError as e:
            pretty_log(
                f"ConnectionRefusedError: Unable to connect to the OPC UA server. Ensure the server is running and the endpoint is correct. Details: {e}"
            )
            self.connected = False
        except asyncio.TimeoutError as e:
            pretty_log(
                f"TimeoutError: The connection attempt to the OPC UA server timed out. Details: {e}"
            )
            self.connected = False
        except Exception as e:
            pretty_log(
                f"An unexpected error occurred while connecting to the OPC UA server: {e}"
            )
            self.connected = False

    async def config(self, recipe):
        if not self.connected:
            raise RuntimeError("Client is not connected. Call start() first.")

        pretty_log(f"Configuring recipe: {recipe}")

        try:
            nsidx = await self.client.get_namespace_index(self.namespace)
            var_node = await self.client.nodes.root.get_child(
                f"0:Objects/{nsidx}:MyObject/{nsidx}:MyVariable"
            )
            await var_node.write_value(
                recipe
            )  # Assuming `recipe` can be written directly
            pretty_log(f"Recipe configured: {recipe}")

        except Exception as e:
            pretty_log(f"An error occurred while configuring the OPC UA server: {e}")

    async def close(self):
        if self.client:
            await self.client.disconnect()
            self.connected = False
