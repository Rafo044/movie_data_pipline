import json
from loguru import logger


async def movie_insert(movie: dict, conn, subscriber_name):
    if conn is None:
        conn = await postgres()
        if conn is None:
            logger.error("No Postgres connection available")
            return
    if subscriber_name == "OMDB":
        await conn.execute(f"""CREATE TABLE IF NOT EXISTS {subscriber_name}_movies (
            imdbID TEXT PRIMARY KEY,
            data JSONB
        );""")

        await conn.execute(
            f"INSERT INTO {subscriber_name}_movies (imdbID, data) VALUES ($1, $2) ON CONFLICT (imdbID) DO NOTHING",
            movie.get("imdbID"),
            json.dumps(movie),
        )
    elif subscriber_name == "TVDB":
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {subscriber_name}_movies (
                id TEXT PRIMARY KEY,
                name TEXT,
                data JSONB
            );
        """)

        await conn.execute(
            f"""
            INSERT INTO {subscriber_name}_movies (id, name, data)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
            """,
            str(movie.get("id")),
            movie.get("name"),
            json.dumps(movie),
        )
