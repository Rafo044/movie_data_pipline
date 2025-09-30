import asyncio
import nats
import os
from nats.js.api import StreamConfig
from dotenv import load_dotenv
from nats.js.errors import ServiceUnavailableError
from loguru import logger


load_dotenv()

JETSTREAM__STREAM_NAME = "movies"
NATS_HOST_PORT_1 = 4222


async def main():
    nc = await nats.connect(f"nats://nats:{NATS_HOST_PORT_1}")

    js = nc.jetstream()
    stream = StreamConfig(
        name=JETSTREAM__STREAM_NAME,
        subjects=[f"{JETSTREAM__STREAM_NAME}.*"],
        storage="memory",
        max_msgs=None,
        max_bytes=None,
        max_age=None,
    )

    for _ in range(10):
        try:
            await js.add_stream(stream)
            logger.info("Stream created")
            break
        except ServiceUnavailableError:
            logger.error("Service unavailable")
            await asyncio.sleep(2)
    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
