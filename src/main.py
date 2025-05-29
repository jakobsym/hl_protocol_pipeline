import logging
import time
import asyncio
from utils.util import merge_dict
from extract.api_extractor import DefiLlamaAPIExtractor, HyperscanAPIExtractor
from extract.blob_extractor import BlobExtractor
from transform.transformer import DefiLlamaJsonTransformer, JsonTokenTransformer
from load.timescale_loader import TimescaleLoader
from utils.logging import config_logging

# init logging
config_logging()
logger = logging.getLogger("main")

async def main():
    start_time = time.time()
    hyperliquid_dexs = ["hyperswap", "valantis", "kittenswap-finance", "laminar"]
    protocol_metrics = {}
    
    """
    - try to avoid running locally to avoid paying for azure blob extraction
    # blob = blob_extractor.fetch_raw_blob_data()
    """    

    blob_extractor = BlobExtractor()
    hs_api_extractor = HyperscanAPIExtractor()
    dl_api_extractor = DefiLlamaAPIExtractor()
    json_transformer = JsonTokenTransformer()
    dl_json_transformer = DefiLlamaJsonTransformer()
    timescale_loader = await TimescaleLoader().establish_timescale_connection_pool()
    
    
    """
    mock_blob =  {'name': 'Hyperswap', 'logoURI': 'https://apricot-real-heron-15.mypinata.cloud/ipfs/QmQqWvMEe3wHRhxAuyDuphVruSXnXXbK8s1CiGkmrJPuKd/hyperswap.jpg', 'keywords': ['audited', 'verified', 'lending'], 'tags': {'stablecoin': {'name': 'Stablecoin', 'description': 'Tokens that are fixed to an external asset'}, 'tokenv1': {'name': 'Hyperswap Token', 'description': 'Genesis Tokens created for the Hyperswap Protocol V1'}}, 'tokens': [{'name': 'Wrapped Hype', 'decimals': 18, 'symbol': 'WHYPE', 'address': '0x5555555555555555555555555555555555555555', 'chainId': 999, 'logoURI': 'https://assets.coingecko.com/coins/images/50882/standard/hyperliquid.jpg?1729431300', 'tags': ['tokenv1']}, {'name': 'Hyperbeat Ultra Hype', 'decimals': 18, 'symbol': 'hbHYPE', 'address': '0x96C6cBB6251Ee1c257b2162ca0f39AA5Fa44B1FB', 'chainId': 999, 'logoURI': 'https://www.hyperbeat.org/assets/images/vaults/hbhype.svg', 'tags': ['tokenv1']}, {'name': 'Reverse Unit Bias', 'decimals': 18, 'symbol': 'RUB', 'address': '0x7DCfFCb06B40344eecED2d1Cbf096B299fE4b405', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/rub.png', 'tags': ['tokenv1']}, {'name': 'HyperFly', 'decimals': 18, 'symbol': 'FLY', 'address': '0x3f244819a8359145a8e7cf0272955e4918a50627', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/FLY_USDC.svg', 'tags': ['tokenv1']}, {'name': 'JEFF', 'decimals': 18, 'symbol': 'JEFF', 'address': '0x52e444545fbE9E5972a7A371299522f7871aec1F', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/JEFF_USDC.svg', 'tags': ['tokenv1']}, {'name': 'SPH800', 'decimals': 18, 'symbol': 'SPH', 'address': '0xd2Fe47eeD2D52725D9e3Ae6df45593837f57C1A2', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/SPH_USDC.svg', 'tags': ['tokenv1']}, {'name': 'CATBAL', 'decimals': 18, 'symbol': 'CATBAL', 'address': '0x11735dBd0B97CfA7Accf47d005673BA185f7fd49', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/CATBAL_USDC.svg', 'tags': ['tokenv1']}, {'name': 'PiP', 'decimals': 18, 'symbol': 'PiP', 'address': '0x1bEe6762F0B522c606DC2Ffb106C0BB391b2E309', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/PIP_USDC.svg', 'tags': ['tokenv1']}, {'name': 'Unit Bitcoin', 'decimals': 8, 'symbol': 'UBTC', 'address': '0x9FDBdA0A5e284c32744D2f17Ee5c74B284993463', 'chainId': 999, 'logoURI': 'https://github.com/user-attachments/assets/67e8fba0-78f6-4a58-8f5a-dbef42007dbc', 'tags': ['tokenv1']}, {'name': 'Looped Hype', 'decimals': 18, 'symbol': 'LHYPE', 'address': '0x5748ae796AE46A4F1348a1693de4b50560485562', 'chainId': 999, 'logoURI': 'https://storage.googleapis.com/stakingrewards-static/images/assets/staging/looped-hype_logo.png?v=1739880923312', 'tags': ['tokenv1']}, {'name': 'Staked Hype', 'decimals': 18, 'symbol': 'stHYPE', 'address': '0xfFaa4a3D97fE9107Cef8a3F48c069F577Ff76cC1', 'chainId': 999, 'logoURI': 'https://github.com/user-attachments/assets/17e8e84d-869f-4853-b080-de829e993b52', 'tags': ['tokenv1']}, {'name': 'Wrapped Staked Hype', 'decimals': 18, 'symbol': 'wstHYPE', 'address': '0x94e8396e0869c9F2200760aF0621aFd240E1CF38', 'chainId': 999, 'logoURI': 'https://github.com/user-attachments/assets/17e8e84d-869f-4853-b080-de829e993b52', 'tags': ['tokenv1']}, {'name': 'KEI Stablecoin', 'decimals': 18, 'symbol': 'KEI', 'address': '0xB5fE77d323d69eB352A02006eA8ecC38D882620C', 'chainId': 999, 'logoURI': 'https://github.com/user-attachments/assets/05bf9af2-f89e-4478-992f-3fa27c7eb873', 'tags': ['tokenv1']}, {'name': 'BULBUL2DAO', 'decimals': 18, 'symbol': 'BULBUL', 'address': '0x99750393c5B40093A53ccD2d8e9f61EF4F401826', 'chainId': 999, 'logoURI': 'https://github.com/user-attachments/assets/2d5b0d9c-a537-4480-b6ff-5264b5d5ab43', 'tags': ['tokenv1']}, {'name': 'alright buddy', 'decimals': 6, 'symbol': 'BUDDY', 'address': '0x47bb061C0204Af921F43DC73C7D7768d2672DdEE', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/buddy.png', 'tags': ['tokenv1']}, {'name': 'SUPERMILK', 'decimals': 6, 'symbol': 'MILK', 'address': '0xFE69bc93B936B34D371defa873686C116C8488c2', 'chainId': 999, 'logoURI': 'https://dd.dexscreener.com/ds-data/tokens/hyperevm/0xfe69bc93b936b34d371defa873686c116c8488c2.png?size=lg&key=076193', 'tags': ['tokenv1']}, {'name': 'feUSD', 'decimals': 18, 'symbol': 'feUSD', 'address': '0x02c6a2fA58cC01A18B8D9E00eA48d65E4dF26c70', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/feUSD.png', 'tags': ['tokenv1']}, {'name': 'Last USD', 'decimals': 18, 'symbol': 'USDXL', 'address': '0xca79db4b49f608ef54a5cb813fbed3a6387bc645', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/usdxl.svg', 'tags': ['tokenv1']}, {'name': 'Purr', 'decimals': 18, 'symbol': 'PURR', 'address': '0x9b498C3c8A0b8CD8BA1D9851d40D186F1872b44E', 'chainId': 999, 'logoURI': 'https://assets.coingecko.com/coins/images/37125/standard/PURR_CG.png', 'tags': ['tokenv1']}, {'name': 'HypurrQuant', 'decimals': 18, 'symbol': 'QUANT', 'address': '0xe443d488a8988262f35b921b36f1c8f5b2fa38e1', 'chainId': 999, 'logoURI': 'https://gray-patient-hamster-834.mypinata.cloud/ipfs/bafkreicfwaztif2ad37kbvqh4frqgotypt7kwcgpqkq4jalwrvpwmmrccm', 'tags': ['tokenv1']}, {'address': '0x04d02CB2E963B4490Ee02b1925223d04F9d83FC6', 'name': 'CAT', 'symbol': 'CAT', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/CAT_USDC.svg', 'tags': ['tokenv1']}, {'address': '0x5804Bf271D9e691611EEA1267B24C1f3D0723639', 'name': 'First AI investment DAO on Hyperliquid', 'symbol': 'HWTR', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/HWTR.png', 'tags': ['tokenv1']}, {'name': 'LIQD', 'decimals': 18, 'symbol': 'LIQD', 'address': '0x1Ecd15865D7F8019D546f76d095d9c93cc34eDFa', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/LIQD.png', 'tags': ['tokenv1']}, {'address': '0xbe6727b535545c67d5caa73dea54865b92cf7907', 'name': 'Unit Ethereum', 'symbol': 'UETH', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/ETH.svg', 'tags': ['tokenv1']}, {'name': 'Magpie Hype', 'decimals': 18, 'symbol': 'mHYPE', 'address': '0xdAbB040c428436d41CECd0Fb06bCFDBAaD3a9AA8', 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/mHYPE.jpg', 'tags': ['tokenv1']}, {'address': '0x6f7e96C0267CD22FE04346aF21f8c6ff54372939', 'name': 'GENESY', 'symbol': 'GENESY', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/GENESY_USDC.svg', 'tags': ['tokenv1']}, {'name': 'Omni X', 'decimals': 18, 'symbol': 'OMNIX', 'address': '0x45eC8F63Fe934C0213476CFb5870835E61dd11FA', 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/OMNIX_USDC.svg', 'tags': ['tokenv1']}, {'address': '0xa320D9f65ec992EfF38622c63627856382Db726c', 'name': 'HFUN', 'symbol': 'HFUN', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/HFUN_USDC.svg', 'tags': ['tokenv1']}, {'address': '0x5d3a1ff2b6bab83b63cd9ad0787074081a52ef34', 'name': 'USDeOFT', 'symbol': 'USDe', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/USDe.jpg', 'tags': ['tokenv1']}, {'address': '0x211cc4dd073734da055fbf44a2b4667d5e5fe5d2', 'name': 'Staked USDe', 'symbol': 'sUSDe', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://raw.githubusercontent.com/HyperSwapX/hyperswap-token-list/refs/heads/main/assets/sUSDe.jpg', 'tags': ['tokenv1']}, {'address': '0x7280CC1f369ab574c35cb8a8D0885e9486e3B733', 'name': 'YEETI', 'symbol': 'YEETI', 'decimals': 18, 'chainId': 999, 'logoURI': 'https://app.hyperliquid.xyz/coins/YEETI_USDC.svg', 'tags': ['tokenv1']}, {'address': '0x6E0F6a71a74fAD5D0ED5A34b468203A4a4437b71', 'name': 'EVMoon', 'symbol': 'EVM', 'decimals': 9, 'chainId': 999, 'logoURI': 'https://dd.dexscreener.com/ds-data/tokens/hyperevm/0x6e0f6a71a74fad5d0ed5a34b468203a4a4437b71.png', 'tags': ['tokenv1']}], 'timestamp': '2025-05-07T15:07:14.353Z', 'version': {'major': 1, 'minor': 3, 'patch': 0}}
    token_blob_data = await blob_extractor.unpack_blob_data(blob=mock_blob)
    token_api_data = hs_api_extractor.fetch_tokens() #TODO: Returns None on some cases?

    token_data = merge_dict(token_api_data, token_blob_data)
    transformed_tokens = json_transformer.transform_token_payload(token_data)
    
    
    # TODO: can this be a function?
    for protocol in hyperliquid_dexs:
        try:
            # extract raw protocol data
            raw_protocol_metrics = dl_api_extractor.collect_protocol_metrics(protocol)

            # transform protocol data
            transformed_protocol_metrics = dl_json_transformer.transform_protocol_metrics(raw_protocol_metrics)

            # load transformed data into a dictionary payload
            protocol_metrics[protocol] = transformed_protocol_metrics
        except Exception as e:
            logger.error("Error processing %s: %s", protocol, str(e))
    
    print(protocol_metrics)
    elapsed_time = (time.time() - start_time) * 1000
    logger.info("Completed batch process in %.2fms", elapsed_time)
    """
if __name__ == "__main__":
    asyncio.run(main())

