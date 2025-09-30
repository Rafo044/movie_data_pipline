import requests
import asyncio
import nats
from dotenv import load_dotenv
import os
from loguru import logger

logger.add("omdb.log")
logger.info("Starting OMDB publisher .....")


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = os.getenv("OMDB_URL")
NATS_HOST_PORT_1 = os.getenv("NATS_HOST_PORT_1")


async def nats_connect():
    try:
        nc = await nats.connect(f"nats:{NATS_HOST_PORT_1}")
        js = nc.jetstream()
        logger.info("Nats server connection established")
    except Exception as e:
        logger.error(f"Nats server connection failed: {e}")


async def omdb_movie_request():
    with open("movies.csv", "r") as file:
        try:
            reder = file.readline()
            response = requests.get(f"{OMDB_URL}{reader}&apikey={OMDB_API_KEY}")
            json_bytes = response.json().encode("utf-8")
            ack = await js.publish("movies.omdb", json_bytes)

            await asyncio.sleep(0.0001)
        except Exception as ex:
            logger.error(f"Dont requests OMDB server .. : {ex}")


async def main():
    task1 = await asyncio.create_task(nats_connect())
    task2 = await asyncio.create_task(omdb_movie_request())

    await task1
    await task2

    logger.info("OMDB movie requests completed")


asyncio.run(main())
