from typing import Dict, Optional
import os
import time
import json
from datetime import datetime

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
    # TODO: Maybe update total_liquidity_timestamp
    def transform_protocol_metrics(self, raw_metics: Dict) -> Dict:
        protocol_name = raw_metics["protocol_name"]
        transformed_metrics = {
            "protocol_name": protocol_name,
            "current_tvl": raw_metics["raw_data"]["current_tvl"],
            "tvl_timestamp": raw_metics["timestamp"],
            "total_liquidity_usd": raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["totalLiquidityUSD"],
            "total_liquidity_timestamp": datetime.fromtimestamp(raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["date"]).isoformat(),
            "current_holdings_usd": raw_metics["raw_data"]["historical_tvl"]["tokensInUsd"][-1]
        }

        if "protocol_volume" in raw_metics["raw_data"]:
            # check if 500 error in volume retrieval
            volume_metric = raw_metics["raw_data"]["protocol_volume"]
            if isinstance(volume_metric, dict) and "500" not in volume_metric and "total24h" in volume_metric:
                transformed_metrics.update({
                    "24h_volume": volume_metric["total24h"],
                    "48h_to_24h_volume": volume_metric["total48hto24h"],
                    "7d_volume": volume_metric["total7d"],
                    "all_time_volume": volume_metric["totalAllTime"]
                })
                
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{protocol_name}_transformed_metrics_{timestamp}.json"
        self._store_data(filename, transformed_metrics)
        return transformed_metrics


    def _store_data(self, filename:str, payload: Dict) -> str:
        """
        Store raw JSON data for reprocessing (if needed)
        """
        filepath = os.path.join(self.transformed_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        return filepath