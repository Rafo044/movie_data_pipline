import asyncio
import nats
from dotenv import load_dotenv
from pathlib import Path
import os
from loguru import logger
import aiohttp
import aiofiles

logger.add("logs/omdb.log")
logger.info("Starting OMDB publisher .....")


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = os.getenv("OMDB_URL")
NATS_PORT_1 = os.getenv("NATS_PORT_1")
MOVIE_CSV_PATH = os.getenv("MOVIE_CSV_PATH")


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


async def omdb_movie_request(nc, js):
    async with aiofiles.open(MOVIE_CSV_PATH, "r") as file:
        async with aiohttp.ClientSession() as session:
            async for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    async with session.get(
                        f"{OMDB_URL}{line}&apikey={OMDB_API_KEY}"
                    ) as response:
                        json_bytes = await response.read()
                        await js.publish(
                            f"movies.omdb",
                            json_bytes,
                            timeout=20,
                        )
                        logger.info(f"{line} published.Next line wait for response")
                except Exception as ex:
                    logger.error(f"OMDB request failed for {line}: {ex}")


async def main():
    nc, js = await nats_connect(NATS_PORT_1)
    await omdb_movie_request(nc, js)
    nc.close()
    logger.info("OMDB movie requests completed")


asyncio.run(main())
