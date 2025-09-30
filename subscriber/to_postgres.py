import asyncio
import nats
from nats.errors import TimeoutError
import polars as pl
import json
from loguru import logger
import os
from dotenv import load_dotenv

# Bir üst qovluqdakı .env faylını yüklə
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

nats_server = os.getenv("NATS_SERVER")
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG") == "True"


async def main():
    nc = await nats.connect("localhost:4222")

    # Create JetStream context.
    js = nc.jetstream()

    # Create pull based consumer on 'foo'.
    subscriber = await js.pull_subscribe("movie_streaming_test.imdb1", "subscriber")

    # Fetch and ack messagess from consumer.
    for i in range(0, 3):
        msgs = await psub.fetch(1)
        for msg in msgs:
            await msg.ack()
            msg_data = msg.data.decode("utf-8")
            df_received = pl.DataFrame(json.loads(msg_data))
            print(df_received)


asyncio.run(main())
