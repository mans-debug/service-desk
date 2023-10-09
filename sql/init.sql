CREATE TABLE IF NOT EXISTS templates
(
    id            SERIAL,
    name          VARCHAR(255) UNIQUE,
    template_text TEXT
);
