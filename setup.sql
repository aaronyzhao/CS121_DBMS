-- Cleans tables if they already exist. Note: warning shown if they
-- don't yet exist.
DROP TABLE IF EXISTS mi_contains;
DROP TABLE IF EXISTS supply_order;
DROP TABLE IF EXISTS cust_order;
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS supplier;

-- Stores information about menu items
CREATE TABLE menu_item (
    menu_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    price_usd NUMERIC(4,2) NOT NULL
);

-- Stores information about suppliers including contact info
CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone CHAR(10) NOT NULL
);

-- Stores information about raw ingredients and their inventory
CREATE TABLE ingredient (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    qty_in_stock NUMERIC(4,2) NOT NULL,
    unit VARCHAR(6),
    supplier_id BIGINT UNSIGNED,
    FOREIGN KEY (supplier_id)
        REFERENCES supplier(supplier_id)
            ON UPDATE CASCADE
);

-- Stores customer orders
CREATE TABLE cust_order (
    co_id SERIAL PRIMARY KEY,
    menu_id BIGINT UNSIGNED NOT NULL,
    qty INT NOT NULL,
    FOREIGN KEY (menu_id)
        REFERENCES menu_item(menu_id)
            ON DELETE CASCADE
);

-- Stores supply orders for more inventory
CREATE TABLE supply_order (
    supply_order_id SERIAL PRIMARY KEY,
    supplier_id BIGINT UNSIGNED,
    status VARCHAR(20) NOT NULL,
    ingredient_id BIGINT UNSIGNED NOT NULL,
    qty INT NOT NULL,
    price_per_unit INT NOT NULL,
    FOREIGN KEY (supplier_id)
        REFERENCES supplier(supplier_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (ingredient_id)
        REFERENCES ingredient(ingredient_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CHECK (status IN ('pending', 'cancelled', 'completed'))
);

-- Stores information about the ingredients in each menu item
CREATE TABLE mi_contains (
    menu_id BIGINT UNSIGNED,
    ingredient_id BIGINT UNSIGNED,
    qty_req NUMERIC(4,2) NOT NULL,
    PRIMARY KEY (menu_id, ingredient_id),
    FOREIGN KEY (menu_id)
        REFERENCES menu_item(menu_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (ingredient_id)
        REFERENCES ingredient(ingredient_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

-- Index on price, which would likely be queried for a lot on the menu
CREATE INDEX price_idx ON menu_item(price_usd)
