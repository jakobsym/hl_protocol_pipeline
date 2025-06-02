from dotenv import load_dotenv
import asyncpg
import asyncio
import os
import logging
from schemas.schemas import HlProtocolMetrics, Tokens

load_dotenv()
logger = logging.getLogger("load")

class TimescaleLoader:
    def __init__(self, connection_str: str = os.getenv("TIMESCALE_CONNECTION_STRING")):
        self.connection_str = connection_str
        self.pool = None

    async def establish_timescale_connection_pool(self, max_retries:int = 3, retry_delay:float = 5):
        attempts = 0
        while attempts < max_retries:
            try:
                self.pool = await asyncpg.create_pool(self.connection_str, command_timeout=60)
                logger.info("DB Connection pool established.")
                return self
            except Exception as e:
                attempt +=1
                if attempt > max_retries:
                    logger.error(f"max retries reached unable to establish timescale connection: {str(e)}")
                    raise
                else:
                    logger.info(f"Retrying in {retry_delay} seconds..")
                    asyncio.sleep(delay=retry_delay)

        
    async def close_connection(self):
        try:
            if self.pool:
                await self.pool.close()
                logger.info("DB Connection is now closed.\n")
        except Exception as e:
            logger.error(f"unable to close timescale connection: {str(e)}")
            raise

    
    async def create_tables(self):
        try:
            async with self.pool.acquire() as conn:
                with open("./src/schemas/tables.sql", 'r') as file:
                    sql_contents = file.read()
                await conn.execute(sql_contents)
            logger.info("table(s) successfully loaded from file")
        except Exception as e:
            logger.error(f"unable to read sql file: {str(e)}")
            raise
    
    # TODO: Finish implementating, currently placeholder
    async def _insert_tokens(self, token_payload: Tokens):
        tokens = token_payload.tokens
            
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    for address, token in tokens.items():
                        token_id = await conn.fetchval('''
                            INSERT INTO tokens (token_address, token_symbol, token_name, supply) VALUES($1, $2, $3, $4)
                            ON CONFLICT (token_address) DO NOTHING
                            RETURNING id;
                        ''',
                        address, token.symbol, token.name, token.supply
                        )
                        # TODO: This looks so ugly
                        if token_id is None:
                            id = await conn.fetchval('''
                                SELECT id FROM tokens WHERE token_address = $1;
                            ''', address)
                            await conn.execute('''
                                INSERT INTO token_metrics (token_id, holders, recorded_at) VALUES($1, $2, $3);
                            ''',
                            id, token.holders,token_payload.timestamp
                            )
                        else:
                            await conn.execute('''
                                INSERT INTO token_metrics (token_id, holders, recorded_at) VALUES($1, $2, $3);
                            ''',
                            token_id, token.holders,token_payload.timestamp
                            )
        except Exception as e:
            logger.error(f"error executing token transaction: {str(e)}")
            raise
        
    async def _insert_protocol_metrics(self, protocol_metrics: HlProtocolMetrics):

        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    for protocol, metrics in protocol_metrics.items():
                        p_id = await conn.fetchval('''
                            INSERT INTO protocols (protocol_name) VALUES($1) ON CONFLICT (protocol_name) DO NOTHING
                            RETURNING ID;
                        ''',
                        protocol)

                        if p_id is None:
                            id = await conn.fetchval('''
                                SELECT id FROM protocols WHERE protocol_name = $1;
                            ''', protocol)
                            await conn.execute('''
                                INSERT INTO protocol_metrics (protocol_id, current_tvl, total_liq_usd, recorded_at)
                                VALUES ($1, $2, $3, $4)
                            ''', id, metrics.current_tvl, metrics.total_liq_usd, metrics.tvl_timestamp)
                        else:
                            await conn.execute('''
                                INSERT INTO protocol_metrics (protocol_id, current_tvl, total_liq_usd, recorded_at)
                                VALUES ($1, $2, $3, $4)
                            ''', p_id, metrics.current_tvl, metrics.total_liq_usd, metrics.tvl_timestamp)
        except Exception as e:
            logger.info(f"error inserting into protocols table: {str(e)}")
            raise

    async def load_into_timescale(self, token_payload: Tokens, protocol_payload: HlProtocolMetrics):
        try:
            await self._insert_tokens(token_payload)
            await self._insert_protocol_metrics(protocol_payload)
            logger.info(f"token and protocol metric(s) payload successfully loaded into Timescale.")
        except Exception as e:
            logger.error(f"error loading payloa(s)) into timescale: {str(e)}")
                   
    
    async def __aenter__(self):
        await self.establish_timescale_connection_pool()
        return self
    
    async def __aexit__(self, type, value, traceback):
        await self.close_connection()