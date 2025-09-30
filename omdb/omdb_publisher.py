import asyncio
import nats
from dotenv import load_dotenv
import os
from loguru import logger
import aiohttp
import aiofiles

logger.add("omdb.log")
logger.info("Starting OMDB publisher .....")


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = os.getenv("OMDB_URL")
NATS_HOST_PORT_1 = os.getenv("NATS_HOST_PORT_1")
MOVIE_CSV_PATH = os.getenv("MOVIE_CSV_PATH")


async def omdb_movie_request():
    try:
        nc = await nats.connect(f"nats:{NATS_HOST_PORT_1}")
        js = nc.jetstream()
        logger.info("Nats server connection established")
        await asyncio.sleep(60)
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

    except Exception as e:
        logger.error(f"Nats server connection failed: {e}")


async def main():
    task = asyncio.create_task(omdb_movie_request())

    await task

    logger.info("OMDB movie requests completed")


asyncio.run(main())
