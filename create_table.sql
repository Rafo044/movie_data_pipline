

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    year INT,
    rated TEXT,
    released DATE,
    runtime TEXT,
    genre TEXT,
    director TEXT,
    writer TEXT,
    actors TEXT,
    plot TEXT,
    language TEXT,
    country TEXT,
    awards TEXT,
    poster TEXT,
    ratings JSONB,
    metascore TEXT,
    imdbrating TEXT,
    imdbvotes TEXT,
    imdbid TEXT,
    type TEXT,
    dvd DATE,
    boxoffice TEXT,
    production TEXT,
    website TEXT
);
