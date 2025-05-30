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

    async def _insert_tokens(self, tokens: Tokens):
        pass

    async def _insert_protocol_metrics(self, protocol_metrics: HlProtocolMetrics):
        pass


    async def load_into_timescale(self, token_payload: Tokens, protocol_payload: HlProtocolMetrics):
        try:
            await self._insert_tokens(token_payload)
            await self._insert_protocol_metrics(protocol_payload)
        except Exception as e:
            logger.error(f"error loading data")
            
        
        
    