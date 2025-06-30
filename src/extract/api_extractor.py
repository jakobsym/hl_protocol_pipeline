from typing import Dict, Optional
import requests
import os
import json
import time
import logging
from datetime import datetime

logger = logging.getLogger("extract")

class HyperscanAPIExtractor:
    def __init__(self, base_url: str = "https://www.hyperscan.com/api/v2", raw_data_dir: str = "../../data/hyperscan_raw_json"):
        self.base_url = base_url
        self.raw_data_dir = raw_data_dir
        self.session = requests.Session()
        self.timeout = 15

        # create raw_json dir if !exist
        self.raw_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), raw_data_dir))
        os.makedirs(self.raw_data_dir, exist_ok=True) # set to true to avoid errors if it exists
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()

        try:
            res = self.session.get(
            url=url,
            params=params,
            timeout=self.timeout,
            headers={"User-Agent": "Python/requests"}
            )

            if res.status_code == 200:
                data =res.json()
                return data
        except Exception as e:
            logger.error("API call failed: %s", str(e), exc_info=True)
            raise
        finally:
            elapsed_time = (time.time() - start_time) * 1000
            logger.info("Completed %s in %.2fms", url, elapsed_time)

    def _store_data(self, filename:str, payload: Dict) -> str:
        """
        Store raw JSON data for reprocessing (if needed)
        """
        filepath = os.path.join(self.raw_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        return filepath
    
    def fetch_tokens(self) -> Dict:
        endpoint = "tokens"
        params = {
            "type": "ERC-20"
        }
        logger.info("Fetching tokens from HyperScan...")
        payload = self._make_request(params=params, endpoint=endpoint)
        # build file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tokens_raw_metrics{timestamp}.json"
        self._store_data(payload=payload, filename=filename)
        return payload
    
        

class DefiLlamaAPIExtractor:
    """ Class for API extraction from Defi Llama API. 
    
    This class provides methods for accessing various endpoints of the 
    Defi Llama API and consolidates all data into a single payload.
    """
    def __init__(self, base_url: str = "https://api.llama.fi", raw_data_dir: str = "../../data/defi_llama_raw_json"):
        self.base_url = base_url
        self.raw_data_dir = raw_data_dir
        self.session = requests.Session()
        self.timeout = 15
        
        # create raw_json dir if !exist
        self.raw_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), raw_data_dir))
        os.makedirs(self.raw_data_dir, exist_ok=True) # set to true to avoid errors if it exists

    def _make_request(self, endpoint: str, method: Optional[str] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()

        try:
            res = self.session.get(
            url=url,
            params=params,
            timeout=self.timeout,
            headers={"User-Agent": "Python/requests"}
            )
            if res.status_code == 200:
                data = res.json()
                return data
            else:
                return {500:"error making request"}
        except Exception as e:
            logger.error("API call failed: %s", str(e), exc_info=True)
            raise # throw exception that was just caught back to caller, exits function 
        finally:
            elapsed = (time.time() - start_time) * 1000
            logger.info("Completed %s in %.2fms", url, elapsed)
            
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
        filename = f"{protocol}_consolidated_raw_metrics_{timestamp}.json"
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
    
    # Returns all holdings for a given protocol as well as historical tvl
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
            
    # returns all protocols on `blockchain` with their daily revenue
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

    
