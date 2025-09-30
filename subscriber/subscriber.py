import asyncio
import nats
from nats.errors import TimeoutError
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

NATS_HOST_PORT_1 = os.getenv("NATS_HOST_PORT_1")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST_PORT = os.getenv("POSTGRES_HOST_PORT")


async def postgres():
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DATABASE,
        host="postgres",
        port=POSTGRES_HOST_PORT,
    )

    await conn.close()


async def omdb_subscriber():
    try:
        nc = await nats.connect(f"nats:{NATS_HOST_PORT_1}")
        js = nc.jetstream()

        sub = await js.subscribe(
            "movies.omdb",
            stream="movies",
            durable="omdb",
            deliver_policy="all",
            manual_ack=True,
        )
        logger.info("Subscriber successfully connected to NATS")
    except Exception as e:
        logger.error(f"Error connecting to NATS: {e}")
        return

    logger.info("Subscriber started, waiting for messages...")

    while True:
        try:
            async for msg in sub.messages:
                print(msg)
                logger.info(f"Received: {msg.data.decode()}")
                await msg.ack()
        except Exception as e:
            logger.info("No message, waiting...")


async def main():
    task = asyncio.create_task(omdb_subscriber())
    await task


asyncio.run(main())
