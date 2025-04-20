from typing import Dict, Optional
import os
import time
from datetime import datetime

class DefiLlamaJsonTransformer:
    """ Class for raw data transformation from Defi Llama

    This class provides methods for transforming raw data into
    structured and validated data.
    """
    def __init__(self, transformed_data_dir: str = "../../data/defi_llama_transformed_data"):
        self.transformed_data_dir = transformed_data_dir

        self.transformed_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), transformed_data_dir))
        os.makedirs(self.transformed_data_dir, exist_ok=True)



    # creates dictionary of current TVL in USD for a protocol
    def transform_protocol_tvl(self, raw_data: Dict) -> Dict:
        return {
            "protocol_name": raw_data["protocol_name"],
            "current_tvl": raw_data["raw_data"]["current_tvl"],
            "timestamp": raw_data["timestamp"]
        }
    

    # returns a dictionary of all relevant metrics for a protocol
    def transform_protocol_metrics(self, raw_metics: Dict) -> Dict:
        return {
            "protocol_name": raw_metics["protocol_name"],
            "current_tvl": raw_metics["raw_data"]["current_tvl"],
            "tvl_timestamp": raw_metics["timestamp"],
            "total_liquidity_usd": raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["totalLiquidityUSD"],
            "total_liquidity_timestamp": datetime.fromtimestamp(raw_metics["raw_data"]["historical_tvl"]["tvl"][-1]["date"]),
            "24h_volume": raw_metics["raw_data"]["protocol_volume"]["total24h"],
            "48h_to_24h_volume": raw_metics["raw_data"]["protcol_volume"]["total48hto24h"],
            "7d_volume": raw_metics["raw_data"]["protcol_volume"]["total7d"],
            "all_time_volume": raw_metics["raw_data"]["protcol_volume"]["totalAllTime"],
            "current_holdings_usd": raw_metics["raw_data"]["historical_tvl"]["tokensInUsd"][-1]
        }
    
    # creates a dictionary of the total amount of liquidity in USD a protocol has
    def current_liquidity_in_usd(self, raw_data: Dict) -> Dict:
        return {
            "protocol_name": raw_data["protocol_name"],
            "total_liquidity_usd": raw_data["raw_data"]["historical_tvl"]["tvl"][-1]["totalLiquidityUSD"],
            "timestamp": datetime.fromtimestamp(raw_data["raw_data"]["historical_tvl"]["tvl"][-1]["date"])
        }

    # creates a dictionary of all volume metrics in USD for a protocol    
    # TODO: Not working currently
    def transform_protocol_volume(self, raw_data: Dict) -> Dict:
        return {
            "protocol_name": raw_data["protocol_name"],
            "24h_volume": raw_data["raw_data"]["protocol_volume"]["total24h"],
            "48h_to_24h_volume": raw_data["raw_data"]["protcol_volume"]["total48hto24h"],
            "7d_volume": raw_data["raw_data"]["protcol_volume"]["total7d"],
            "all_time_volume": raw_data["raw_data"]["protcol_volume"]["totalAllTime"]
        }
    
    # creates dictionary of all tokens a DEX currently holds denominated in USD
    def tokens_in_usd_value(self, raw_data: Dict) -> Dict:
        return {
            "protocol_name": raw_data["protocol_name"],
            "current_holdings_usd": raw_data["raw_data"]["historical_tvl"]["tokensInUsd"][-1]
        }
        
    
        
