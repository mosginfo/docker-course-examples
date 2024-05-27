CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    parent_id INT REFERENCES category(id)
);

INSERT INTO category (name, parent_id)
VALUES
    ('Настольные компьютеры', NULL),
    ('Ноутбуки', NULL),
    ('Комплектующие', NULL),
    ('Материнские платы', 3),
    ('Процессоры', 3),
    ('Оперативная память', 3);
