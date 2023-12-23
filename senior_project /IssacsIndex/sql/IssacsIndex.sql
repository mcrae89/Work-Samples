-- DROP DATABASE IF EXISTS "IssacsIndex";

-- CREATE DATABASE "IssacsIndex";

-- \c IssacsIndex

DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Ratings;
DROP TABLE IF EXISTS Prices;
DROP TABLE IF EXISTS Products;

CREATE TABLE Products (
    id SERIAL NOT NULL,
    identifier VARCHAR(255) DEFAULT NULL, -- product_id from Serpapi
    product_name VARCHAR(255) UNIQUE NOT NULL, -- Title from Serpapi
    product_description TEXT DEFAULT NULL, -- snippet from Serpapi
    keywords TEXT DEFAULT NULL, -- extensions from Serpapi
    issacs_insight INTEGER DEFAULT 0,
    source_url TEXT DEFAULT NULL, -- Link from chrome extension
    img TEXT DEFAULT NULL, -- Thumbnail from serpapi
    last_updated_date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TABLE Prices (
    id SERIAL NOT NULL,
    product_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL, -- extracted_price from serpapi
    price_url TEXT UNIQUE, -- link from serpapi
    retailer TEXT, -- source from serpapi
    last_updated_date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Ratings (
    id SERIAL NOT NULL,
    product_id INT NOT NULL,
    avg_rating DECIMAL(2,1) NOT NULL, -- rating from serpapi
    number_of_ratings INT NOT NULL, -- reviews from serpapi
    last_updated_date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Reviews (
    id  SERIAL NOT NULL,
    product_id INT NOT NULL,
    source VARCHAR(255), -- username and review website; source from serpapi
    title TEXT,
    review TEXT,
    review_date TIMESTAMP,
    last_updated_date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE EXTENSION IF NOT EXISTS pg_trgm;