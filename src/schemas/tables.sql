CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    token_address TEXT UNIQUE NOT NULL,
    token_symbol TEXT,
    holders INTEGER,
    supply BIGINT
);

CREATE TABLE IF NOT EXISTS protocols (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocol_name TEXT UNIQUE NOT NULL,
    current_tvl DECIMAL,
    current_tvl_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    total_liq_usd DECIMAL,
    total_liq_usd_timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

-- is this even relevant to store?
-- To view all holdings for a given protocol you simply
-- join based on the ids for a specific protocol
CREATE TABLE IF NOT EXISTS protocol_holdings (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocol_id INTEGER REFERENCES protocols(id),
    token_id INTEGER REFERENCES tokens(id),
    holdings_usd DECIMAL NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);


CREATE INDEX IF NOT EXISTS idx_protocol_holdings_token ON protocol_holdings(token_address);
CREATE INDEX IF NOT EXISTS idx_token_holders ON tokens(holders);

