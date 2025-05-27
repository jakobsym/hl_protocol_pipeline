from dotenv import load_dotenv
import asyncpg
import asyncio
import os

load_dotenv()


class TimescaleLoader:
    def __init__(self, connection_str: str = os.getenv("TIMESCALE_CONNECTION_STRING")):
        pass