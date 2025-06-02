from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    holders: Optional[int] = None
    supply: Optional[int] = None

class Tokens(BaseModel):
    timestamp: datetime
    tokens: dict[str, Token]
    @field_validator('timestamp')
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class TokenHoldings(BaseModel):
    date: int
    tokens: dict[str, float]

class HlProtocolMetrics(BaseModel):
    protocol_name: str
    current_tvl: float
    tvl_timestamp: datetime = None
    total_liq_usd: float
    total_liq_timestamp: datetime = None
    current_holdings_usd: TokenHoldings
    volume_24h: Optional[float] = None
    volume_48h_to_24h: Optional[float] = None
    volume_7d: Optional[float] = None
    all_time_volume: Optional[float] = None

    # converts timestamps into datetime objects from strings
    @field_validator('tvl_timestamp', 'total_liq_timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


