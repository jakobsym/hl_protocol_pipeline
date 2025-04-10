from typing import Dict, Optional
import requests

class DefiLlamaAPIExtractor:
    """ Class for API extraction from Defi Llama API. 
    
    This class provides methods for accessing various endpoints of the 
    Defi Llama API.
    """
    def __init__(self, base_url: str = "https://api.llama.fi"):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 30

    def _make_request(self, endpoint: str, method: Optional[str] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
                
        res = self.session.get(
            url=url,
            params=params,
            timeout=self.timeout
        )

        if res.status_code == 200:
            return res.json()
        else:
            return {500:"error making request"}
        
    def get_dex_vol_summary(self, protocol: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyVolume"):
        endpoint = f"summary/dexs/{protocol}"

        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }

        return self._make_request(endpoint, params=params)

    def get_all_protocols_fee_and_revenue(self, blockchain: str):
        endpoint = f"overview/fees/{blockchain}"
        return self._make_request(endpoint=endpoint)
    
    # return dictionary of all protocols and assciated daily fees
    # or is this done in transmforation stage?
    def get_protocols_daily_fees(self, blockchain: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyFees"):
        endpoint = f"overview/fees/{blockchain}"
        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }
        return self._make_request(endpoint=endpoint, params=params)
        
    # def get_protocols_total_fees() -> Dict:

    # def get_protocols_total_revenue() -> Dict:
        
    def get_protocols_daily_revenue(self, blockchain: str, exclude_total_data_chart: bool = True, exlcude_total_data_chart_breakdown: bool = None, data_type: str = "dailyRevenue") -> Dict:
        protocol_daily_revenue = {}
        endpoint = f"overview/fees/{blockchain}"
        params = {
            "excludeTotalDataChart": str(exclude_total_data_chart).lower(),
            "excludeTotalDataChartBreakdown": str(exlcude_total_data_chart_breakdown).lower(),
            "dataType": data_type
        }
        return self._make_request(endpoint=endpoint, params=params)

    def get_historical_protocol_tvl(self, protocol: str):
        endpoint = f"protocol/{protocol}"
        return self._make_request(endpoint=endpoint)

    def get_current_protocol_tvl(self, protocol: str):
        endpoint = f"tvl/{protocol}"
        return self._make_request(endpoint=endpoint)
    
    def get_historical_chain_tvl(self, blockchain: str):
        endpoint = f"v2/historicalChainTvl/{blockchain}"
        return self._make_request(endpoint=endpoint)