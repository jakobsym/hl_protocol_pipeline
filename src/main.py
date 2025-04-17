from extract.api_extractor import DefiLlamaAPIExtractor
# from transform.dl_api_transformer import DefiLlamaJsonTransformer

# TODO: 'valantis' and 'kittenswap-finance' are not listed within Defi llama dexs
def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance"]
    # blockchains = ["hyperliquid l1"]
    
    dl_api_extractor = DefiLlamaAPIExtractor()
    #dl_json_transformer = DefiLlamaJsonTransformer()

    for protocol in hyperliquid_dexs:
        try:
            # extract raw data
            print(f"    Extracting {protocol} data...")
            protocol_metric = dl_api_extractor.collect_protocol_metrics(protocol)

            # transform raw data
            # transformed_data = dl_json_transformer.transform_collected_data(protocol_metric)
    
            # load transformed data into storage
        except Exception as e:
            print(f"  ERROR processing {protocol}: {str(e)}")
        

if __name__ == "__main__":
    main()

