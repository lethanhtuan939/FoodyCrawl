CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    city_id INTEGER UNIQUE NOT NULL,
    country_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    country_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    categories TEXT[] NOT NULL,
    cuisines TEXT[] NOT NULL,
    address VARCHAR(255) NOT NULL,
    rating_avg FLOAT NOT NULL,
    rating_total_review INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    is_open BOOLEAN NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES locations(city_id) ON DELETE SET NULL
);