/*
2.1 Получение информации о сумме товаров заказанных под каждого клиента
(Наименование клиента, сумма)
*/
SELECT clients.name,
    COALESCE(SUM(order_items.unit_price * order_items.quantity), 0)
      AS total_amount
FROM clients
LEFT JOIN orders ON clients.id = orders.client_id
LEFT JOIN order_items ON orders.id = order_items.order_id
GROUP BY clients.id, clients.name
ORDER BY total_amount DESC;

/*
2.2. Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.
*/
SELECT categories.id, categories.name,
COUNT(category_trees.depth) AS first_level_count
FROM categories
LEFT JOIN category_trees ON category_trees.ancestor_id = categories.id
    AND category_trees.depth = 1
GROUP BY categories.id, categories.name
ORDER BY categories.id ASC;

/*
2.3.1. Написать текст запроса для отчета (view)
«Топ-5 самых покупаемых товаров за последний месяц» (по количеству штук в заказах).
В отчете должны быть:
Наименование товара, Категория 1-го уровня, Общее количество проданных штук.
*/
SELECT
    products.id,
    products.name AS product,
    categories.name AS cat_name,
    SUM(order_items.quantity) AS total_quantity
FROM products
JOIN order_items ON order_items.product_id = products.id
JOIN orders ON orders.id = order_items.order_id
JOIN category_trees ON category_trees.descendant_id = products.category_id
    AND category_trees.depth = 1
JOIN categories ON categories.id = category_trees.ancestor_id
--WHERE orders.create_date >= CURRENT_TIMESTAMP - interval '30 days' -- PostgreSQL variant
WHERE orders.create_date >= datetime('now', '-30 days')  -- SQLite variant
GROUP BY products.id, products.name, categories.name
ORDER BY total_quantity DESC
LIMIT 5;
