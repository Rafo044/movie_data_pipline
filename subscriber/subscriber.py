import asyncio
from loguru import logger
from subscriber.insert_to_postgres import movie_insert
import json
from nats_connection import nats_connection_check
from postgres import postgres

logger.add("logs/consumer.log")


async def receiver(
    subscriber_name,
    subject_name,
    consumer_name,
):
    nc, js = await nats_connection_check()

    sub = await js.subscribe(
        f"movies.{subject_name}",
        durable=f"{consumer_name}",
        deliver_policy="all",
        manual_ack=True,
    )

    logger.info(f"{subscriber_name} subscriber started, waiting for messages...")

    while True:
        try:
            async for msg in sub.messages:
                logger.info(f"{subscriber_name} message received")
                try:
                    conn = await postgres()
                    movie_dict = json.loads(msg.data.decode())
                    await movie_insert(
                        conn=conn, subscriber_name=subscriber_name, movie=movie_dict
                    )
                    await msg.ack()
                    logger.info("Movie inserted into PostgreSQL")
                except Exception as e:
                    logger.error(f"Error inserting movie into PostgreSQL: {e}")
        except Exception as e:
            logger.info(f"{subscriber_name} no message, waiting...")


async def main():
    task = receiver(subject_name="tvdb", subscriber_name="TVDB", consumer_name="demo7")
    await task


asyncio.run(main())
