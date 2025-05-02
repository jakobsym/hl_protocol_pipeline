from extract.api_extractor import DefiLlamaAPIExtractor, HyperscanAPIExtractor
from transform.transformer import DefiLlamaJsonTransformer
from utils.logging import config_logging

# init logging
config_logging()

def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance", "laminar"]
    # blockchains = ["hyperliquid l1"]
    hs_api_extractor = HyperscanAPIExtractor()
    dl_api_extractor = DefiLlamaAPIExtractor()
    dl_json_transformer = DefiLlamaJsonTransformer()

    for protocol in hyperliquid_dexs:
        try:
            """
            # extract raw data
            protocol_metrics = dl_api_extractor.collect_protocol_metrics(protocol)

            # transform raw data
            #print(f"    Transforming {protocol} raw data...\n")
            transformed_metrics = dl_json_transformer.transform_protocol_metrics(protocol_metrics)
            
            # load transformed data into storage
            """
        except Exception as e:
            print(f"  \nERROR processing {protocol}: {str(e)}")
        

if __name__ == "__main__":
    main()

