from extract.api_extractor import DefiLlamaAPIExtractor

# TODO: 'valantis' and 'kittenswap-finance' are not listed within Defi llama dexs
def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance"]
    # blockchains = ["hyperliquid l1"]
    dl_api_extractor = DefiLlamaAPIExtractor()

    """
    payload = []
    for dexs in hyperliquid_dexs:
        res = dl_api_extractor.consolidate_protocol_metrics(dexs)
        print(res["protocol_name"])
        print(res["raw_data"]["protocol_volume"])
        payload.append(res)
    print(payload)
    """   
    
if __name__ == "__main__":
    main()

