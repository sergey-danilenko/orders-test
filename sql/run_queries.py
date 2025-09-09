import asyncio
import re
import sqlite3
from pathlib import Path
from typing import Any

from tabulate import tabulate

from app.common.config import Config, Paths
from app.common.config import load_config
from app.common.config import get_paths


def parse_sql_file(file_path):
    content = Path(file_path).read_text(encoding='utf-8')
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    queries = []
    current_query = ""

    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('--') or not line:
            continue
        current_query = current_query + "\n" + line
        if line.endswith(";"):
            queries.append(current_query.strip())
            current_query = ""

    return queries


def run_sql(
    cursor: sqlite3.Cursor,
    data: dict[str, Any],
):
    cursor.execute(data["sql"])
    results = cursor.fetchall()

    table_name = data["table_name"]
    print(table_name)
    print("=" * len(table_name))
    print(tabulate(results, headers=data["headers"], tablefmt="grid"), end="\n\n")


SQL_DATA = [
    {
        "table_name": "Информации о сумме товаров заказанных под каждого клиента",
        "headers": ["Наименование клиента", "сумма"],
        "sql": """
            SELECT clients.name,
            COALESCE(SUM(order_items.unit_price * order_items.quantity), 0)
              AS total_amount
            FROM clients
            LEFT JOIN orders ON clients.id = orders.client_id
            LEFT JOIN order_items ON orders.id = order_items.order_id
            GROUP BY clients.id, clients.name
            ORDER BY total_amount DESC;
        """

    },
    {
        "table_name": (
            "Количество дочерних элементов первого уровня вложенности"
            "для категорий номенклатуры"
        ),
        "headers": ["Категория", "Кол-во дочерних элементов"],
        "sql": """
            SELECT categories.id, categories.name,
            COUNT(category_trees.depth) AS first_level_count
            FROM categories
            LEFT JOIN category_trees ON category_trees.ancestor_id = categories.id
                AND category_trees.depth = 1
            GROUP BY categories.id, categories.name
            ORDER BY categories.id ASC;
        """,
    },
    {
        "table_name": "«Топ-5 самых покупаемых товаров за последний месяц»",
        "headers": [
            "Наименование товара",
            "Категория 1-го уровня",
            "Общее количество проданных штук",
        ],
        "sql": """
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
        """,
    },
]


async def main():
    paths: Paths = get_paths()
    config: Config = load_config(paths)
    conn = sqlite3.connect(paths.app_dir / config.db.dbname)
    cursor = conn.cursor()
    for data in SQL_DATA:
        run_sql(cursor, data)

    cursor.close()


if __name__ == "__main__":
    asyncio.run(main())
