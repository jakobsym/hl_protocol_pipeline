CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    token_address TEXT UNIQUE NOT NULL,
    token_symbol TEXT,
    token_name TEXT,
    supply NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS token_metrics(
    token_id INTEGER REFERENCES tokens(id),
    holders INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY(token_id, recorded_at)
);

CREATE TABLE IF NOT EXISTS protocols (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocol_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS protocol_metrics(
    protocol_id INTEGER REFERENCES protocols(id),
    current_tvl DECIMAL,
    total_liq_usd DECIMAL,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY(protocol_id, recorded_at)
);


-- create hypertable (not needed yet)
--SELECT create_protocol_hypertable('protocol_metrics', 'recorded_at')
--SELECT create_token_hypertable('token_holder_metrics', 'recorded_at')

-- create views

-- create indexes
CREATE INDEX IF NOT EXISTS idx_tokens_id ON tokens(id);
CREATE INDEX IF NOT EXISTS idc_token_metrics_holders ON token_metrics(holders);
