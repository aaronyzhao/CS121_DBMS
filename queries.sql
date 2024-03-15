-- a. Join between `menu_item` and `mi_contains` to get the ingredients
-- for a specific menu item:

SELECT mi.name AS menu_item_name, i.name AS ingredient_name, mc.qty_req
    FROM menu_item mi
    JOIN mi_contains mc ON mi.menu_id = mc.menu_id
    JOIN ingredient i ON mc.ingredient_id = i.ingredient_id
    WHERE mi.menu_id = 1; -- Example for menu item with menu_id = 1


-- b. Join between `supplier`, `ingredient`, and `supply_order` to list supply
-- orders with supplier and ingredient details:
-- Note: Got Empty Set
SELECT s.name AS supplier_name, i.name AS ingredient_name, so.qty, 
    so.price_per_unit, so.status
    FROM supply_order so
    JOIN supplier s ON so.supplier_id = s.supplier_id
    JOIN ingredient i ON so.ingredient_id = i.ingredient_id;
    
    

-- c. Join between `cust_order`, `menu_item`, and `mi_contains` to list 
-- customer orders with menu item names and the quantity of ingredients 
-- required

SELECT co.co_id, mi.name AS menu_item_name, i.name AS ingredient_name, 
   (co.qty * mc.qty_req) AS total_qty_required
   FROM cust_order co
   JOIN menu_item mi ON co.menu_id = mi.menu_id
   JOIN mi_contains mc ON mi.menu_id = mc.menu_id
   JOIN ingredient i ON mc.ingredient_id = i.ingredient_id;

-- b. Join Involving a Complex Condition
-- Query to list suppliers and the total quantity of each ingredient they need
-- to fulfill all current orders, considering the quantity required for each menu item in customer orders:
SELECT s.name AS supplier_name, i.name AS ingredient_name, SUM(co.qty * mc.qty_req) AS total_qty_required
    FROM supplier s
    JOIN ingredient i ON s.supplier_id = i.supplier_id
    JOIN mi_contains mc ON i.ingredient_id = mc.ingredient_id
    JOIN cust_order co ON mc.menu_id = co.menu_id
    GROUP BY s.name, i.name;
    
    
-- c. Multi-Level Join with Conditional Aggregation
-- Find the total cost of supply orders for each supplier, differentiated by status 
-- (e.g., 'pending', 'completed'):
-- Note: Got Empty Set
SELECT s.name, so.status, SUM(so.qty * so.price_per_unit) AS total_cost
    FROM supplier s
    JOIN supply_order so ON s.supplier_id = so.supplier_id
    GROUP BY s.name, so.status;