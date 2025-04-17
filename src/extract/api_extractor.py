from typing import Dict, Optional
import requests
import os
import json
import time
from datetime import datetime

class DefiLlamaAPIExtractor:
    """ Class for API extraction from Defi Llama API. 
    
    This class provides methods for accessing various endpoints of the 
    Defi Llama API and consolidates all data into a single payload.
    """
    def __init__(self, base_url: str = "https://api.llama.fi", raw_data_dir: str = "../../data/defi_llama_raw_json"):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 1
        self.raw_data_dir = raw_data_dir

        # create raw_json dir if !exist
        self.raw_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), raw_data_dir))
        os.makedirs(self.raw_data_dir, exist_ok=True) # set to true to avoid errors if it exists

    def _make_request(self, endpoint: str, method: Optional[str] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            res = self.session.get(
            url=url,
            params=params,
            timeout=self.timeout
            )
            if res.status_code == 200:
                data = res.json()
                return data
            else:
                return {500:"error making request"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def _store_data(self, filename:str, payload: Dict) -> str:
        """
        Store raw JSON data for reprocessing (if needed)
        """
        filepath = os.path.join(self.raw_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        return filepath
            
    def collect_protocol_metrics(self, protocol: str) -> Dict:
        protocol_data = {
            "protocol_name": protocol,
            "raw_data": {},
            "timestamp": datetime.now().isoformat(),
            "errors": [] # track any possible failed request(s)
        }

        # iterate through list of tuples collecting all metrics
        metrics = [
            ("protocol_volume", self.get_dex_vol_summary, {"protocol":protocol}),
            ("current_tvl", self.get_current_protocol_tvl, {"protocol":protocol}),
            ("historical_tvl", self.get_historical_protocol_tvl, {"protocol":protocol})
        ]

        for metric, method, params in metrics:
            try:
                time.sleep(self.timeout)
                payload = method(**params)
                # error check payload
                if isinstance(payload, dict) and "error" in payload:
                    protocol_data["errors"].append({"metric": metric, "error": payload["error"]})
                else:
                    protocol_data["raw_data"][metric] = payload
                
            except Exception as e:
                protocol_data["errors"].append({"metric": metric, "error": str(e)})
        # store raw payload
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{protocol}_consolidated_data_{timestamp}.json"
        self._store_data(filename, protocol_data)
        return protocol_data


    """ 
    Returns (24h vol, 48h-24h vol, 7d vol, all-time vol)
    """
    def get_dex_vol_summary(self, protocol: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyVolume"):
        endpoint = f"summary/dexs/{protocol}"

        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }

        return self._make_request(endpoint, params=params)
    
    def get_historical_protocol_tvl(self, protocol: str):
        endpoint = f"protocol/{protocol}"
        return self._make_request(endpoint=endpoint)

    def get_current_protocol_tvl(self, protocol: str):
        endpoint = f"tvl/{protocol}"
        return self._make_request(endpoint=endpoint)

    def get_all_protocols_fee_and_revenue(self, blockchain: str):
        endpoint = f"overview/fees/{blockchain}"
        return self._make_request(endpoint=endpoint)
    
    # returns all protocols on `blockchain` with their daily fees
    def get_protocols_daily_fees(self, blockchain: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyFees"):
        endpoint = f"overview/fees/{blockchain}"
        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }
        return self._make_request(endpoint=endpoint, params=params)
            
    # returns all protocols on `blockchain` with their daily fees
    def get_protocols_daily_revenue(self, blockchain: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyRevenue") -> Dict:
        protocol_daily_revenue = {}
        endpoint = f"overview/fees/{blockchain}"
        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }
        return self._make_request(endpoint=endpoint, params=params)
    
    def get_historical_chain_tvl(self, blockchain: str):
        endpoint = f"v2/historicalChainTvl/{blockchain}"
        return self._make_request(endpoint=endpoint)

    
