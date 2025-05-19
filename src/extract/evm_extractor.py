import logging
import json
import time
from web3 import Web3
from web3.types import BlockData

logger = logging.getLogger("extract")

class HyperEvmBlockExtractor:
    def __init__(self, rpcNode: str = "https://rpc.hyperliquid.xyz/evm"):
        self.rpcNode = rpcNode
    
    def _connect_to_rpc(self) -> Web3:
        try:
            return Web3(Web3.HTTPProvider(self.rpcNode))
        except Exception as e:
            logger.error(f"Failed to establish rpc connection, {str(e)}")
            raise

        
    def _load_erc20_contract_abi(self):
        try:
            with open('./src/config/abi.json', 'r') as f:
                abi = json.load(f)
                logger.info(f"Successfully loaded ERC-20 ABI with {len(abi)}")
            return abi
        except Exception as e:
            logger.error(f"Failed to load ERC-20 ABI: {str(e)}")
            raise
    
    def _get_token_info(self, tokenAddress: str, rpcConnection: Web3):
        erc20_abi = self._load_erc20_contract_abi()

        try:
            token_contract = rpcConnection.eth.contract(address=tokenAddress, abi=erc20_abi)
            name = token_contract.functions.name().call()
            symbol = token_contract.functions.symbol().call()
            total_supply = token_contract.functions.totalSupply().call()

            return {
            "name": name,
            "symbol": symbol,
            "total_supply": total_supply
        }

        except Exception as e:
            logger.error(f"Failed to get token_info: {str(e)}")
            raise

    def read_evm(self) -> list:
        token_list = []
        connection = self._connect_to_rpc()
        
        block = connection.eth.get_block('latest', full_transactions=True)

        for tx_hash in block.transactions:
            tx_receipt = connection.eth.get_transaction_receipt(tx_hash['hash'])
            if tx_receipt["contractAddress"]:
                token_info = self._get_token_info(tx_receipt["contractAddress"], connection)
                token_list.append(token_info)

        return token_list
            
        


        