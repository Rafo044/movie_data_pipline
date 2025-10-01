from dotenv import load_dotenv
from pathlib import Path
import asyncpg
import os
from loguru import logger


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
NATS_PORT_1 = os.getenv("NATS_PORT_1")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


async def postgres():
    try:
        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DATABASE,
            host="localhost",
            port=POSTGRES_PORT,
        )
        logger.info("Postgres connection established")
        return conn
    except Exception as e:
        logger.error(f"Postgres connection failed: {e}")
        return None
