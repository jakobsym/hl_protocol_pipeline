from dotenv import load_dotenv
import asyncpg
import asyncio
import os
import logging
from schemas.schemas import HlProtocolMetrics, Tokens

load_dotenv()
logger = logging.getLogger("load")

# TODO: Seperate some of these methods
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
                logger.info("DB Connection is now closed.")
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
                        res = await conn.fetchval('''
                            INSERT INTO tokens (token_address, token_symbol, token_name, supply) VALUES($1, $2, $3, $4)
                            ON CONFLICT (token_address) DO NOTHING
                            RETURNING id;
                        ''',
                        address, token.symbol, token.name, token.supply
                        )

                        await conn.execute('''
                            INSERT INTO token_metrics (token_id, holders, recorded_at) VALUES($1, $2, $3);
                        ''',
                        res, token.holders,token_payload.timestamp
                        )
        except Exception as e:
            logger.error(f"error executing token transaction: {str(e)}")
            raise
        

    # TODO: Finish implementating, currently placeholder
    async def _insert_protocol_metrics(self, protocol_metrics: HlProtocolMetrics):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO protocols VALUES($1 $2);
                ''',
                protocol_metrics.current_tvl,
                )
        except Exception as e:
            logger.info(f"error inserting into protocols table: {str(e)}")
            raise

            #  protocol_payload: HlProtocolMetrics
    async def load_into_timescale(self, token_payload: Tokens):
        try:
            await self._insert_tokens(token_payload)
            #await self._insert_protocol_metrics(protocol_payload)
            logger.info(f"token and protocol metric(s) payload successfully loaded into Timescale.")
        except Exception as e:
            logger.error(f"error loading payloa(s)) into timescale: {str(e)}")
                   
    
    async def __aenter__(self):
        await self.establish_timescale_connection_pool()
        return self
    
    async def __aexit__(self, type, value, traceback):
        await self.close_connection()