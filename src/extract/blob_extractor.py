import json
from socket import timeout
import aiohttp
import asyncio
import os
import logging
from typing import Dict
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger("extract")
load_dotenv()

class BlobExtractor:
    def __init__(self, conn_str: str = os.getenv("AZURE_CONNECTION_STRING"), container_name: str = "token-data"):
        self.conn_str = conn_str
        self.container_name = container_name
    
    # returns a blob in JSON format
    def fetch_raw_blob_data(self) -> Dict:
        try:
            logger.info("Fetching blob data...")
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=self.conn_str)
            container_client = blob_service_client.get_container_client(self.container_name)

            # list all blobs in container
            blobs = list(container_client.list_blobs(name_starts_with="builds/"))

            json_blobs = [blob for blob in blobs if blob.name.endswith("tokens.json")]
            if not json_blobs:
                return "No JSON files within container"

            # find most recent blob
            latest_blob = max(json_blobs, key=lambda x: x.last_modified)
            
            blob_client = container_client.get_blob_client(latest_blob.name)

            download_stream = blob_client.download_blob()
            content = download_stream.readall()

            json_content = json.loads(content)
            #logger.info(f"Blob content: {json_content}")
            return json_content
        except Exception as e:
            logger.error("Failed to fetch blob data: %s", str(e), exc_info=True)
            raise

    #calls hyperscan api for e/a token to get its holders and (WIP) supply
    # this is only for tokens that are not apart of other payload
    async def unpack_blob_data(self, blob: Dict) -> dict:
        tokens = blob["tokens"]
        token_data_list = []
        transformed_tokens = {}
        try:
            logger.info("Unpacking blob data...")
            tasks = [self.fetch_token_data(token) for token in tokens]
            token_data_list = await asyncio.gather(*tasks)

            transformed_tokens["items"] = token_data_list
            logger.info("Completed unpacking blob data...\n")
            return transformed_tokens
        except Exception as e:
            logger.error("Unpacking blob data failed: %s", str(e), exc_info=True)
            raise

    
    
    async def fetch_token_data(self, token: Dict) -> dict:
        holders = await self.fetch_token_holders(token["address"]) 
        token_supply = await self.fetch_supply(token["address"])
        return {
            "address": token["address"],
            "symbol": token["symbol"],
            "name": token["name"],
            "holders": holders,
            "total_supply": token_supply
        }

    # TODO: Possibly relocate these methods as these are transforming the given data
    # TODO: Add logging
    # TODO: These run so slow, can that be fixed?
    async def fetch_token_holders(self, token_address: str) -> int:
        url = f"https://hyperscan.gas.zip/api/v2/tokens/{token_address}/counters"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    if res.status == 200:
                        data = await res.json()
                        await asyncio.sleep(3) #TODO: This can increased in prod
                        return int(data["token_holders_count"])
                    return -1
        except Exception as e:
            logger.error("API call failed fetching token holders: %s", str(e), exc_info=True)
            raise

    # TODO: conditional logic seems off here, can probably rewrite
    # TODO: Add logging
    async def fetch_supply(self, token_address: str) -> int:
        url = f"https://hyperscan.gas.zip/api/v2/tokens/{token_address}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    if res.status != 200:
                        return -1
                    data = await res.json()
                    if data["total_supply"] != None:
                        await asyncio.sleep(3.5)
                        return int(data["total_supply"])
                    else:
                        return -1
        except Exception as e:
            logger.error("API call failed fetching token supply: %s", str(e), exc_info=True)
            raise