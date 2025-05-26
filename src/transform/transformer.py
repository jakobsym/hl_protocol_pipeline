from typing import Dict
import os
import json
import logging
import time
import itertools
from datetime import datetime
from schemas.schemas import HlProtocolMetrics, Tokens

logger = logging.getLogger("transform")

class JsonTokenTransformer:
    

    def __init__(self, transformed_data_dir: str = "../../data/hyperscan_transformed_data"):
        self.transformed_data_dir = transformed_data_dir
        self.id_iter = itertools.count()
        self.id = next(self.id_iter)

        # create transformed data directory
        self.transformed_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), transformed_data_dir))
        os.makedirs(self.transformed_data_dir, exist_ok=True)

    def transform_token_payload(self, payload: Dict) -> Tokens:
        start_time = time.time()
        tokens = payload["items"]
        transformed_tokens = {}
        
        try:
            for token in tokens:
                if token["symbol"] == None or token["symbol"] == "Claim: hyperliquid-labs.com":
                    continue
                transformed_tokens[token["address"]] = {
                    "symbol": token["symbol"],
                    "name": token["name"],
                    "holders": int(token["holders"]), 
                    "supply": int(token["total_supply"])
                    }
                
            # validate transformed_tokens
            self.id = next(self.id_iter)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            validated_tokens = Tokens(tokens=transformed_tokens, timestamp=timestamp, batch_id=self.id)
            
            filename = f"transformed_token_metrics_{timestamp}.json"
            self._store_data(filename, transformed_tokens)

            return validated_tokens
        except Exception as e:
            logger.error("processing failed for %s: %s", token, str(e), exc_info=True)
            raise
        finally:
            elapsed_time = (time.time() - start_time) * 1000
            logger.info("Completed transformation in %.2fms\n", elapsed_time)


    def _store_data(self, filename:str, payload: Dict) -> str:
        """
        Store raw JSON data for reprocessing (if needed)
        """
        filepath = os.path.join(self.transformed_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        return filepath


            
        


class DefiLlamaJsonTransformer:
    """ Class for raw data transformation from Defi Llama

    This class provides methods for transforming raw data into
    structured and validated data.
    """
    def __init__(self, transformed_data_dir: str = "../../data/defi_llama_transformed_data"):
        self.transformed_data_dir = transformed_data_dir

        # create transformed data directory
        self.transformed_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), transformed_data_dir))
        os.makedirs(self.transformed_data_dir, exist_ok=True)


    # returns a dictionary of all relevant metrics for a protocol
    def transform_protocol_metrics(self, raw_metics: Dict) -> HlProtocolMetrics:
        start_time = time.time()
        try:
            protocol_name = raw_metics["protocol_name"]
            transformed_metrics = {
                "protocol_name": protocol_name,
                "current_tvl": raw_metics["raw_data"]["current_tvl"],
                "tvl_timestamp": raw_metics["timestamp"],
                "total_liq_usd": raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["totalLiquidityUSD"],
                "total_liq_timestamp": datetime.fromtimestamp(raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["date"]).isoformat(),
                "current_holdings_usd": raw_metics["raw_data"]["historical_tvl"]["tokensInUsd"][-1]
            }

            if "protocol_volume" in raw_metics["raw_data"]:
                # check if 500 error in volume retrieval
                volume_metric = raw_metics["raw_data"]["protocol_volume"]
                if isinstance(volume_metric, dict) and "500" not in volume_metric and "total24h" in volume_metric:
                    transformed_metrics.update({
                        "volume_24h": volume_metric["total24h"],
                        "volume_48h_to_24h": volume_metric["total48hto24h"],
                        "volume_7d": volume_metric["total7d"],
                        "all_time_volume": volume_metric["totalAllTime"]
                    })
            # validate transformed_metrics
            metrics = HlProtocolMetrics(**transformed_metrics)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{protocol_name}_transformed_metrics_{timestamp}.json"
            self._store_data(filename, transformed_metrics)
            return metrics
        except Exception as e:
            logger.error("processing failed for %s: %s", protocol_name, str(e), exc_info=True)
            raise
        finally:
            elapsed = (time.time() - start_time) * 1000
            logger.info("Completed transformation in %.2fms\n", elapsed)
    
    def _store_data(self, filename:str, payload: Dict) -> str:
        """
        Store raw JSON data for reprocessing (if needed)
        """
        filepath = os.path.join(self.transformed_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        return filepath