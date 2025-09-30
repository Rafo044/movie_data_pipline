from pydantic import BaseModel, root_validator


class ImdbMovie(BaseModel):
    pass

    class Config:
        extra: "ignore"
