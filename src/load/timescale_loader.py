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

    # TODO: Retry logic?
    async def establish_timescale_connection_pool(self) -> asyncpg.Pool:
        try:
            self.pool = await asyncpg.create_pool(self.connection_str)
            return self
        except Exception as e:
            logger.error(f"unable to establish timescale connection: {str(e)}")
            raise
    
    async def _close_connection(self):
        try:
            if self.pool:
                await self.pool.close()
        except Exception as e:
            logger.error(f"unable to close timescale connection: {str(e)}")
            raise

    
    async def create_tables(self, connection_pool: asyncpg.Pool):
        try:
            async with connection_pool.acquire() as conn:
                with open("../schemas/tables.sql", 'r') as file:
                    sql_contents = file.read()
                await conn.execute(sql_contents)
            await connection_pool.close()
            logger.info("table(s) successfully loaded from file")
        except Exception as e:
            logger.error(f"unable to read sql file: {str(e)}")
            raise

    async def load_into_timescale(self, token_payload: Tokens, protocol_payload: HlProtocolMetrics):
        pass
    