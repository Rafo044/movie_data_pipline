from pydantic import BaseModel, root_validator


class TmdbMovie(BaseModel):
    pass

    class Config:
        extra: "ignore"
