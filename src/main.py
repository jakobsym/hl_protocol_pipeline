from extract.api_extractor import DefiLlamaAPIExtractor

def main():
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance"]
    blockchains = ["hyperliquid l1"]
    api_extractor = DefiLlamaAPIExtractor()
    dex_vol = api_extractor.get_dex_vol_summary("hyperswap")
    
    print(dex_vol)

if __name__ == "__main__":
    main()