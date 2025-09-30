import asyncio
import nats
from nats.js.api import StreamConfig


async def main():
    nc = await nats.connect("nats://localhost:4222")

    js = nc.jetstream()
    stream = StreamConfig(
        name="movie_streaming_test",
        subjects=["movie_streaming_test.*"],
        storage="memory",
        max_msgs=20,
        max_bytes=None,
        max_age=None,
    )

    await js.add_stream(stream)

    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
