from pydantic import BaseModel, root_validator


class TvdbMovie(BaseModel):
    name: str
    slug: str
    image: str
    nameTranslations: list[dict[str, str]]
    overviewTranslations: list[dict[str, str]]
    aliases: list[str]
    firstAired: str
    lastAired: str
    nextAired: str
    score: float
    status: str
    originalCountry: str
    originalLanguage: str
    defaultSeasonType: str
    isOrderRandomized: bool
    lastUpdated: int
    averageRuntime: int
    episodes: int
    overview: str
    year: int

    @root_validator(pre=True)
    def normalize_keys(cls, values):
        with open("mapping.txt", "r") as file:
            mapping = file.read()
            new_values = {}
            for k, v in values.items():
                new_key = mapping.get(k, k)  # tapırsa dəyiş, tapmırsa olduğu kimi saxla
                new_values[new_key] = v
        return new_values

    class Config:
        extra: "ignore"
