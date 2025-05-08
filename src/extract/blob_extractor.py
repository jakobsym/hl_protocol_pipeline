import json
import requests
import os
import logging
from typing import Dict
from dotenv import load_dotenv
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

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
            logger.info(f"Blob content: {json_content}")
            return json_content
        except Exception as e:
            logger.error("Failed to fetch blob data: %s", str(e), exc_info=True)
            raise

    #calls hyperscan api for e/a token to get its holders and (WIP) supply
    # this is only for tokens that are not apart of other payload
    def fetch_token_data(self, blob: Dict) -> Dict:
        tokens = blob["tokens"]
        semi_transformed_tokens = {}

        for token in tokens:
            semi_transformed_tokens[token["address"]] = {
                "symbol": token["symbol"],
                "name": token["name"],
                "holders": self.fetch_token_holders(token["address"])
            }
        
        return semi_transformed_tokens

            
            
    def fetch_token_holders(self, token_address: str) -> int:
        session = requests.Session()
        url = f"https://hyperscan.gas.zip/api/v2/tokens/{token_address}/counters"

        try:
            res = session.get(url=url, timeout=0.5)
            if res.status_code == 200:
                data = res.json()
                return int(data["token_holders_count"])
        except Exception as e:
            logger.error("API call failed: %s", str(e), exc_info=True)
            raise