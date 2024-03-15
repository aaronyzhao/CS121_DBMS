drop FUNCTION IF EXISTS calculate_total_order_cost;
drop FUNCTION IF EXISTS get_supplier_contact_for_ingredient;

drop PROCEDURE IF EXISTS insert_new_customer_order;
drop PROCEDURE IF EXISTS update_ingredient_inventory;
drop PROCEDURE IF EXISTS process_supply_order;

drop TRIGGER IF EXISTS before_supply_order_update;

-- UDF FUNCTIONS
-- 1. Calculate Total Order Cost
-- This function calculates the total cost of a customer order by multiplying 
-- the quantity of menu items ordered by their price and summing the results
--  for an order.
DELIMITER !

CREATE FUNCTION calculate_total_order_cost(co_id BIGINT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_cost DECIMAL(10,2);
    SELECT SUM(mi.price_usd * co.qty) INTO total_cost
    FROM cust_order co
    JOIN menu_item mi ON co.menu_id = mi.menu_id
    WHERE co.co_id = co_id;
    RETURN total_cost;
END! 

DELIMITER ;

-- 2. Find Supplier Contact for Ingredient
-- This function returns the contact information of the supplier for a given 
-- ingredient.
DELIMITER !

CREATE FUNCTION get_supplier_contact_for_ingredient(ingredient_id BIGINT)
RETURNS VARCHAR(115) -- Name, email, and phone concatenated
DETERMINISTIC
BEGIN
    DECLARE contact_info VARCHAR(115);
    SELECT CONCAT(s.name, ' - Email: ', s.email, ', Phone: ', s.phone) 
        INTO contact_info
    FROM supplier s
    JOIN ingredient i ON s.supplier_id = i.supplier_id
    WHERE i.ingredient_id = ingredient_id;
    RETURN contact_info;
END!

DELIMITER ;


-- Part 2  Procedure
-- Procedure
-- 1. Insert New Customer Order
-- This procedure inserts a new customer order into the cust_order table.
DELIMITER !

CREATE PROCEDURE insert_new_customer_order
    (IN menu_id_param BIGINT UNSIGNED, IN qty_param INT)
BEGIN
    INSERT INTO cust_order(menu_id, qty) VALUES (menu_id_param, qty_param);
END !

DELIMITER ;

-- 2. Update Ingredient Inventory
-- This procedure updates the inventory level for a specific ingredient.
DELIMITER !

CREATE PROCEDURE update_ingredient_inventory
    (IN ingredient_id_param BIGINT UNSIGNED, IN qty_in_stock_param NUMERIC(4,2))
BEGIN
    UPDATE ingredient
    SET qty_in_stock = qty_in_stock_param
    WHERE ingredient_id = ingredient_id_param;
END!

DELIMITER ;


-- 3. Process Supply Order
-- This procedure changes the status of a supply order and can be adapted to 
-- include more functionality such as adjusting inventory levels upon order completion.
DELIMITER !

CREATE PROCEDURE process_supply_order
    (IN supply_order_id_param BIGINT UNSIGNED, IN status_param VARCHAR(20))
BEGIN
    UPDATE supply_order
    SET status = status_param
    WHERE supply_order_id = supply_order_id_param;
END!

DELIMITER ;


-- Trigger
DELIMITER !

CREATE TRIGGER after_cust_order_insert
AFTER INSERT ON cust_order
FOR EACH ROW
BEGIN
    -- Temporary table to hold required ingredient quantities for 
    -- the ordered menu item
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE v_ingredient_id BIGINT UNSIGNED;
    DECLARE v_qty_required NUMERIC(4,2);

    DECLARE cur CURSOR FOR
        SELECT ingredient_id, qty_req * NEW.qty AS qty_required
        FROM mi_contains
        WHERE menu_id = NEW.menu_id;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    -- Open the cursor
    OPEN cur;

    fetch_loop: LOOP
        -- Get the next ingredient
        FETCH cur INTO v_ingredient_id, v_qty_required;
        IF finished = 1 THEN 
            LEAVE fetch_loop;
        END IF;

        -- Update the ingredient quantity in stock
        UPDATE ingredient
        SET qty_in_stock = qty_in_stock - v_qty_required
        WHERE ingredient_id = v_ingredient_id;

    END LOOP fetch_loop;

    -- Close the cursor
    CLOSE cur;
END!

DELIMITER ;




-- UDF TESTS
-- 1. Calculate Total Order Cost of cust_id 1
SELECT calculate_total_order_cost(1) AS total_order_cost;

-- 2. Find Supplier Contact for Ingredient
-- ingredient_id = 1 here
SELECT get_supplier_contact_for_ingredient(1) AS supplier_contact;


-- PROCEDURE TESTS
-- 1. Insert 5 of menu_id 1
CALL insert_new_customer_order(1, 5);

-- 2. Update ingredient_id = 1 by 10 uniuts
CALL update_ingredient_inventory(1, 10.00);

-- 3. Adjust supply_order_id = 1 to completed
CALL process_supply_order(1, 'completed');

-- TRIGGER TESTS
-- cookie should go from 3 -> 0 units
-- cust_order 102 bc insert_new_customer_order is 101
SELECT * FROM ingredient;
INSERT INTO cust_order VALUES (102, 13, 3);
SELECT * FROM ingredient;


