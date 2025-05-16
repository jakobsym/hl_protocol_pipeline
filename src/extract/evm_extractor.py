import logging
import time
from web3 import Web3
from web3.types import BlockData

logger = logging.getLogger("extract")

class HyperEvmBlockExtractor:
    def __init__(self, rpcNode: str = "https://rpc.hyperliquid.xyz/evm"):
        self.rpcNode = rpcNode
    
    def _connect_to_rpc(self) -> Web3:
        return Web3(Web3.HTTPProvider(self.rpcNode))
    
    def read_evm(self) -> BlockData:
        tx_list = []
        connection = self._connect_to_rpc()
        block = connection.eth.get_block('latest', full_transactions=True)

        for tx_hash in block.transactions:
            tx_receipt = connection.eth.get_transaction_receipt(tx_hash['hash'])
            tx_list.append(tx_receipt)

        return tx_list
            
        


        