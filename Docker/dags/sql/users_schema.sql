CREATE TABLE IF NOT EXISTS users (
    firstname VARCHAR(60) NOT NULL,
    lastname VARCHAR(60) NOT NULL,
    country VARCHAR(60) NOT NULL,
    username VARCHAR(60) NOT NULL,
    password VARCHAR(60) NOT NULL,
    email VARCHAR(60) PRIMARY KEY NOT NULL
    );