import logging
import time
from extract.api_extractor import DefiLlamaAPIExtractor, HyperscanAPIExtractor
from transform.transformer import DefiLlamaJsonTransformer, HyperScanJsonTransformer
from utils.logging import config_logging

# init logging
config_logging()
logger = logging.getLogger("main")

def main():
    start_time = time.time()
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance", "laminar"]
    # blockchains = ["hyperliquid l1"]

    hs_api_extractor = HyperscanAPIExtractor()
    hs_json_transformer = HyperScanJsonTransformer()
    dl_api_extractor = DefiLlamaAPIExtractor()
    dl_json_transformer = DefiLlamaJsonTransformer()

    tokens = hs_api_extractor.fetch_tokens()
    transformed_tokens = hs_json_transformer.transform_token_payload(tokens)
    
    for protocol in hyperliquid_dexs:
        try:
            
            # extract raw data
            protocol_metrics = dl_api_extractor.collect_protocol_metrics(protocol)

            # transform raw data
            #print(f"    Transforming {protocol} raw data...\n")
            transformed_metrics = dl_json_transformer.transform_protocol_metrics(protocol_metrics)
            
            # load transformed data into storage
        except Exception as e:
            print(f"  \nERROR processing {protocol}: {str(e)}")

    elapsed_time = (time.time() - start_time) * 1000
    logger.info("Completed batch process in %.2fms", elapsed_time)
            
if __name__ == "__main__":
    main()

