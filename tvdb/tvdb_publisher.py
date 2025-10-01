import tvdb_v4_official
from loguru import logger
import asyncio
import nats
from dotenv import load_dotenv
from pathlib import Path
import os
import json

logger.add("tvdb.log")
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TVDB_PIN = os.getenv("TVDB_PIN")
TVDB_API_KEY = os.getenv("TVDB_API_KEY")
NATS_PORT_1 = os.getenv("NATS_PORT_1")


async def nats_connect(port, retries=3, delay=1):
    for attempt in range(1, retries + 1):
        try:
            nc = await nats.connect(f"nats://localhost:{port}", connect_timeout=5)
            js = nc.jetstream()
            logger.info(" NATS server connection established")
            return nc, js
        except Exception as e:
            logger.error(f"NATS connection attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    raise RuntimeError("Could not connect to NATS after multiple attempts")


async def tvdb_request():
    logger.info("Starting TVDB API streaming.....")
    tvdb = tvdb_v4_official.TVDB(TVDB_API_KEY, pin=TVDB_PIN)
    return tvdb


async def tvdb_series_info(js, tvdb, total_range=3):
    for j in range(total_range):
        try:
            all_series = tvdb.get_all_series(j)
            for series in all_series:
                json_bytes = json.dumps(series).encode("utf-8")
                ack = await js.publish("movies.tvdb", json_bytes)

            logger.info(f"Published:{ack}")
        except Exception as e:
            logger.error(f"Error publishing TVDB series info: {e}")


async def main():
    nc, js = await nats_connect(NATS_PORT_1)

    tvdb = await tvdb_request()

    await tvdb_series_info(total_range=10, js=js, tvdb=tvdb)

    await nc.close()
    logger.info("Completed TVDB series info streaming.....")


asyncio.run(main())
