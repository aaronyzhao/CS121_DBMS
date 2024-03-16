-- a. Join between `menu_item` and `mi_contains` to get the ingredients
-- for a specific menu item:
-- !! RELATIONAL ALGEBRA #2 !!
SELECT mi.name AS menu_item_name, i.name AS ingredient_name, mc.qty_req
    FROM menu_item mi
    JOIN mi_contains mc ON mi.menu_id = mc.menu_id
    JOIN ingredient i ON mc.ingredient_id = i.ingredient_id
    WHERE mi.menu_id = 1; -- Example for menu item with menu_id = 1
    
-- b. For all customer orders, list the menu_item_name and ALL corresponding
-- ingredients required (by name) and total quantity needed for that order
SELECT co.co_id, mi.name AS menu_item_name, i.name AS ingredient_name, 
   (co.qty * mc.qty_req) AS total_qty_required
   FROM cust_order co
   JOIN menu_item mi ON co.menu_id = mi.menu_id
   JOIN mi_contains mc ON mi.menu_id = mc.menu_id
   JOIN ingredient i ON mc.ingredient_id = i.ingredient_id;

-- c. List supplier_name, ingredient_name, qty, price_per_unit and status
SELECT s.name AS supplier_name, i.name AS ingredient_name, so.qty, 
    so.price_per_unit, so.status
    FROM supply_order so
    JOIN supplier s ON so.supplier_id = s.supplier_id
    JOIN ingredient i ON so.ingredient_id = i.ingredient_id;
    
-- d. Find the total cost of supply orders for each supplier, differentiated 
-- by status (e.g., 'pending', 'completed'); sort of a follow up function
-- to query c
SELECT s.name, so.status, SUM(so.qty * so.price_per_unit) AS total_cost
    FROM supplier s
    JOIN supply_order so ON s.supplier_id = so.supplier_id
    GROUP BY s.name, so.status;

-- e. Delete a supply order (example here being supply_order_id = 1)
-- !! RELATIONAL ALGEBRA #3 !!
DELETE FROM supply_order
    WHERE supply_order_id = 1; 

-- f. Find all menu items below $10
SELECT name, description, price_usd
    FROM menu_item
    WHERE price_usd < 10.00
    ORDER BY price_usd ASC;
