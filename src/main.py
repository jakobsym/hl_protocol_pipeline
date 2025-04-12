from extract.api_extractor import DefiLlamaAPIExtractor

def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance"]
    blockchains = ["hyperliquid l1"]
    dl_api_extractor = DefiLlamaAPIExtractor()
    
    dex_vol = dl_api_extractor.get_dex_vol_summary(protocol="hyperswap")
    # current_tvl = dl_api_extractor.get_current_protocol_tvl(protocol="hyperswap")
    # hist_tvl = dl_api_extractor.get_historical_protocol_tvl(protocol="hyperswap")

    print(dex_vol["total24h"])
    
if __name__ == "__main__":
    main()