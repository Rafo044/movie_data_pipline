import asyncio
import nats
import os
from nats.js.api import StreamConfig
from dotenv import load_dotenv
from nats.js.errors import ServiceUnavailableError
from loguru import logger
from pathlib import Path


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
NATS_PORT_1 = os.getenv("NATS_PORT_1")


async def main():
    nc = await nats.connect(
        servers=f"nats://localhost:{NATS_PORT_1}", connect_timeout=20
    )

    js = nc.jetstream()
    stream = StreamConfig(
        name="movies",
        subjects=["movies.*"],
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
