import asyncio
import nats
from loguru import logger
import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
NATS_PORT_1 = os.getenv("NATS_PORT_1")


async def nats_connection_check(port=NATS_PORT_1, retries=3, delay=1):
    for attempt in range(1, retries + 1):
        try:
            nc = await nats.connect(f"nats://localhost:{port}")
            js = nc.jetstream()
            logger.info(" NATS server connection established")
            return nc, js
        except Exception as e:
            logger.error(f"NATS connection attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    raise RuntimeError("Could not connect to NATS after multiple attempts")
