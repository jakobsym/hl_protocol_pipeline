from extract.api_extractor import DefiLlamaAPIExtractor

def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance"]
    # blockchains = ["hyperliquid l1"]
    dl_api_extractor = DefiLlamaAPIExtractor()

    res = dl_api_extractor.consolidate_protocol_metrics("hyperswap")
    print(res)

    """
    data = {}
    dex_vol = dl_api_extractor.get_dex_vol_summary(protocol="hyperswap")
    current_tvl = dl_api_extractor.get_current_protocol_tvl(protocol="hyperswap")
    hist_tvl = dl_api_extractor.get_historical_protocol_tvl(protocol="hyperswap")

    data["dex_vol"] = dex_vol
    data["current_tvl"] = current_tvl
    data["hist_tvl"] = hist_tvl
    print(data)
    """

    """
    payload = []
    for dexs in hyperliquid_dexs:
        res = dl_api_extractor.consolidate_protocol_metrics(dexs)
        payload.append(res)

    print(payload)    
    """
    
    
if __name__ == "__main__":
    main()