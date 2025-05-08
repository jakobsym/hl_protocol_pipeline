import logging
import time
from extract.api_extractor import DefiLlamaAPIExtractor, HyperscanAPIExtractor
from extract.blob_extractor import read_blob
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
    dl_api_extractor = DefiLlamaAPIExtractor()
    hs_json_transformer = HyperScanJsonTransformer()
    dl_json_transformer = DefiLlamaJsonTransformer()

    tokens = hs_api_extractor.fetch_tokens()
    transformed_tokens = hs_json_transformer.transform_token_payload(tokens)
    
    for protocol in hyperliquid_dexs:
        try:
            # extract raw data
            protocol_metrics = dl_api_extractor.collect_protocol_metrics(protocol)

            # transform raw data
            transformed_metrics = dl_json_transformer.transform_protocol_metrics(protocol_metrics)
            
            # load transformed data into storage
            
        except Exception as e:
            logger.error("Error processing %s: %s", protocol, str(e))

    # TODO: Create a payload that contains all transformed data that gets loaded in 1 stage, so there is not so many DB calls
    elapsed_time = (time.time() - start_time) * 1000
    logger.info("Completed batch process in %.2fms", elapsed_time)
            
if __name__ == "__main__":
    main()

