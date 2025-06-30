import psycopg2
import os
import logging
import asyncio
from dotenv import load_dotenv
from schemas.schemas import HlProtocolMetrics, Tokens

load_dotenv()
logger = logging.getLogger("load")

class SupabaseLoader:
    def __init__(self, connection_str: str = os.getenv("SUPABASE_CONNECTION_STRING")):
        self.connection_str = connection_str
        self.connection = None
    
    async def establish_supabase_connection(self, max_retries=3, retry_delay= 5.0):
        attempts = 0
        while attempts < max_retries:
            try:
                self.connection = psycopg2.connect(self.connection_str)
                logger.info("Supabase connection established")
                return self
            except Exception as e:
                attempt += 1
                if attempt > max_retries:
                    logger.error(f"max retries reached unable to establish timescale connection: {str(e)}")
                    raise
                else:
                    logger.info(f"Retrying in {retry_delay} seconds..")
                    asyncio.sleep(delay=retry_delay)

    async def close_supabase_connection(self):
        try:
            if self.connection:
                await self.connection.close()
                logger.info("Supabase connection is now closed\n")
        except Exception as e:
            logger.error(f"unable to close supabase connection: {str(e)}")
            raise
    
    async def _insert_tokens(self, token_payload: Tokens):
        pass

    async def _insert_protocol_metrics(self, protocol_metrics: HlProtocolMetrics):
        pass

    async def load_into_supabase(self, token_payload:Tokens, protocol_payload: HlProtocolMetrics):
        try:
            await self._insert_tokens(token_payload=token_payload)
            await self._insert_protocol_metrics(protocol_metrics=protocol_payload)
        except Exception as e:
            logger.error(f"error loading payload(s) into supabase: {str(e)}")
        
    async def __aenter__(self):
        await self.establish_supabase_connection()
        return self
    
    async def __aexit__(self, type, value, traceback):
        await self.close_supabase_connection()
        