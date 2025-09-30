from pydantic import BaseModel, root_validator


class OmdbMovie(BaseModel):
    title: str
    year: int
    rated: str
    released: str
    runtime: str
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: str
    ratings: list[dict[str, str]]
    metascore: str
    imdbrating: str
    imdbvotes: str
    imdbid: str
    type: str
    dvd: str
    boxoffice: str
    production: str
    website: str

    class Config:
        extra: "ignore"
