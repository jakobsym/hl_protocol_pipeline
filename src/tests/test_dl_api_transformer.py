import pytest
from transform.transformer import DefiLlamaJsonTransformer
from schemas.schemas import HlProtocolMetrics

class TestDefiLlamaJsonTransformer:
    @pytest.fixture
    def transformer(self):
        return DefiLlamaJsonTransformer()

    def test_transformation_with_volume(self, transformer):
        raw_metrics = {
                "protocol_name": "test_protocol",
                "timestamp": "2025-04-28T14:01:49.755928",
                "raw_data": {
                    "protocol_volume": {
                        "total24h": 500,
                        "total48hto24h": 400,
                        "total7d": 2000,
                        "totalAllTime": 10000
                    },
                    "current_tvl": 1000.0,
                    "historical_tvl": {
                        "tvl": [{"totalLiquidityUSD": 900.0, "date": 1745864027}],
                        "tokensInUsd": [{"date": 1745864027, "tokens": {"TEST": 100.0}}]
                    }
                }
            }

        res = transformer.transform_protocol_metrics(raw_metrics)

        assert res.protocol_name == "test_protocol"
        assert res.volume_24h == 500.0
        assert res.volume_48h_to_24h == 400.0
        assert res.volume_7d == 2000.0
        assert res.all_time_volume == 10000.0
    
    def test_transformation_with_volume_error(self, transformer):
        raw_metrics = {
                "protocol_name": "test_protocol",
                "timestamp": "2025-04-28T14:01:49.755928",
                "raw_data": {
                    "protocol_volume": {
                        "500": "error making request"
                    },
                    "current_tvl": 1000.0,
                    "historical_tvl": {
                        "tvl": [{"totalLiquidityUSD": 900.0, "date": 1745864027}],
                        "tokensInUsd": [{"date": 1745864027, "tokens": {"TEST": 100.0}}]
                    }
                }
            }
    
        res = transformer.transform_protocol_metrics(raw_metrics)

        assert res.protocol_name == "test_protocol"
        assert res.volume_24h == None
        assert res.volume_48h_to_24h == None
        assert res.volume_7d == None
        assert res.all_time_volume == None

    def test_transformation_without_volume(self, transformer):
        raw_metrics = {
                "protocol_name": "test_protocol",
                "timestamp": "2025-04-28T14:01:49.755928",
                "raw_data": {
                    "current_tvl": 1000.0,
                    "historical_tvl": {
                        "tvl": [{"totalLiquidityUSD": 900.0, "date": 1745864027}],
                        "tokensInUsd": [{"date": 1745864027, "tokens": {"TEST": 100.0}}]
                    }
                }
            }
    
        res = transformer.transform_protocol_metrics(raw_metrics)

        assert res.protocol_name == "test_protocol"
        assert res.volume_24h == None
        assert res.volume_48h_to_24h == None
        assert res.volume_7d == None
        assert res.all_time_volume == None