CREATE TABLE tokens IF NOT EXISITS (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    token_address UNIQUE TEXT NOT NULL,
    token_symbol TEXT,
    holders INTEGER,
    supply BIGINT
);

CREATE TABLE protocols IF NOT EXISITS (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocol_name UNIQUE TEXT NOT NULL,
    current_tvl DECIMAL,
    current_tvl_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    total_liq_usd DECIMAL,
    total_liq_usd_timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE protocol_holdings IF NOT EXISITS (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocol_id UNIQUE INTEGER REFERENCES protocols(id),
    token_address UNIQUE TEXT REFERENCES tokens(token_address),
    holdings_usd DECIMAL NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);