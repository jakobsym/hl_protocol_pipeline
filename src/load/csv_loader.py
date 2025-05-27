import os
from schemas.schemas import HlProtocolMetrics, Tokens

class CSVFileLoader:

    def __init__(self, hl_token_csv_dir: str = "../../data/hl_tokens.csv", hl_protocol_csv_dir = "../../data/hl_protocols.csv"):
        self.hl_token_csv_dir = hl_token_csv_dir
        self.hl_protocol_csv_dir = hl_protocol_csv_dir

        self.hl_token_csv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), hl_token_csv_dir))
        self.hl_protocol_csv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), hl_protocol_csv_dir))
        os.makedirs(self.hl_token_csv_dir, exist_ok=True)
        os.makedirs(self.hl_protocol_csv_dir, exist_ok=True)

    def _ingest_token_payload(self, token_payload: Tokens):
        pass

    def _ingest_protocol_payload(self, protocol_payload: HlProtocolMetrics):
        pass