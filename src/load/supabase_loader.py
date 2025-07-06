import psycopg2
import os
import logging
import time
from dotenv import load_dotenv
from schemas.schemas import HlProtocolMetrics, Tokens

load_dotenv()
logger = logging.getLogger("load")

class SupabaseLoader:
    def __init__(self, connection_str: str = os.getenv("SUPABASE_CONNECTION_STRING")):
        self.connection_str = connection_str
        self.connection = None
    
    def establish_supabase_connection(self, max_retries=3, retry_delay= 5.0):
        attempts = 0
        while attempts < max_retries:
            try:
                self.connection = psycopg2.connect(self.connection_str)
                logger.info("Supabase connection established")
                return self
            except Exception as e:
                attempts += 1
                if attempts > max_retries:
                    logger.error(f"max retries reached unable to establish timescale connection: {str(e)}")
                    raise
                else:
                    logger.info(f"Retrying in {retry_delay} seconds..")
                    time.sleep(retry_delay)

    def close_supabase_connection(self):
        try:
            if not self.connection is None:
                if not self.connection.closed:
                    self.connection.close()
                    logger.info("Supabase connection is now closed\n")
        except Exception as e:
            logger.error(f"unable to close supabase connection: {str(e)}")
        

    def create_tables(self):
        try:
            with self.connection.cursor() as curs:
                with open("./src/schemas/tables.sql", 'r') as file:
                    sql_contents = file.read()
                curs.execute(sql_contents)
                self.connection.commit()
            logger.info("table(s) successfully loaded from file")
        except Exception as e:
            logger.error(f"unable to read sql file: {str(e)}")
            raise

    def _insert_tokens(self, token_payload: Tokens):
        tokens = token_payload.tokens

        try:
            self.connection.autocommit = False
            with self.connection.cursor() as curs:
                try:
                    for address, token in tokens.items():
                        curs.execute('''
                            INSERT INTO tokens (token_address, token_symbol, token_name, supply) 
                                VALUES(%s, %s, %s, %s)
                                ON CONFLICT (token_address) DO NOTHING
                                RETURNING id;
                            ''',
                            (address, token.symbol, token.name, token.supply))
                        token_id = curs.fetchone()[0] if curs.rowcount > 0 else None

                        if token_id is None:
                            curs.execute('''
                                SELECT id FROM tokens WHERE token_address = %s;
                            ''', (address,))
                            id = curs.fetchone()[0]
                            curs.execute('''
                                INSERT INTO token_metrics (token_id, holders, recorded_at) 
                                VALUES(%s, %s, %s);
                            ''',
                            (id, token.holders, token_payload.timestamp))
                        else:
                            curs.execute('''
                                INSERT INTO token_metrics (token_id, holders, recorded_at) 
                                VALUES(%s, %s, %s);
                            ''',
                            (token_id, token.holders, token_payload.timestamp))
                    self.connection.commit()
                    logger.info(f"successfully inserted token metrics")
                except Exception as e:
                    self.connection.rollback() # rollback commit on error
                    raise
        except Exception as e:
            logger.error(f"error executing token transaction: {str(e)}")
            raise
        finally:
            curs.close()
            self.connection.autocommit = True




    def _insert_protocol_metrics(self, protocol_metrics: HlProtocolMetrics):
        try:
            self.connection.autocommit = False
            with self.connection.cursor() as curs:
                try:
                    for protocol, metrics in protocol_metrics.items():
                        curs.execute('''
                            INSERT INTO protocols (protocol_name) VALUES(%s) ON CONFLICT (protocol_name) DO NOTHING
                            RETURNING ID;
                        ''', (protocol,))
                        p_id = curs.fetchone()[0] if curs.rowcount > 0 else None

                        if p_id is None:
                            curs.execute('''
                                SELECT id FROM protocols WHERE protocol_name = %s;
                            ''', (protocol))
                            id = curs.fetchone()[0]
                            curs.execute('''
                                INSERT INTO protocol_metrics (protocol_id, current_tvl, total_liq_usd, recorded_at)
                                VALUES (%s, %s, %s, %s)
                            ''', (id, metrics.current_tvl, metrics.total_liq_usd, metrics.tvl_timestamp))
                        else:
                            curs.execute('''
                                INSERT INTO protocol_metrics (protocol_id, current_tvl, total_liq_usd, recorded_at)
                                VALUES (%s, %s, %s, %s)
                            ''', (p_id, metrics.current_tvl, metrics.total_liq_usd, metrics.tvl_timestamp))
                    self.connection.commit()
                    logger.info(f"successfully inserted protocol metrics")
                except Exception as e:
                    self.connection.rollback()
                    raise       
        except Exception as e:
            logger.error(f"error executing protocol transaction: {str(e)}")
            raise
        finally:
            curs.close()
            self.connection.autocommit = True


    def load_into_supabase(self, token_payload:Tokens):
        try:
            self._insert_tokens(token_payload=token_payload)
            #self._insert_protocol_metrics(protocol_metrics=protocol_payload)
        except Exception as e:
            logger.error(f"error loading payload(s) into supabase: {str(e)}")
        
    def __enter__(self):
        return self.establish_supabase_connection()
        
    def __exit__(self, type, value, traceback):
        self.close_supabase_connection()