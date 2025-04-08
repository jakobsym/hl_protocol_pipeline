from extract.api_extractor import DefiLlamaAPIExtractor

def main():
    api_extractor = DefiLlamaAPIExtractor()
    dex_vol = api_extractor.get_dex_vol_summary("hyperswap")
    
    print(dex_vol)

if __name__ == "__main__":
    main()