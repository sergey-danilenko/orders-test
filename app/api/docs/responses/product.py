from app.api.utils.response_factory import ResponseFactory

factory = ResponseFactory()

PRODUCT_LIST = factory.ok(
    example=
    [
        {
            "id": 1,
            "name": "Холодильник Aceline",
            "category_id": 4,
            "stock_quantity": 9,
            "price": 18999,
            "create_date": "2025-09-09T06:35:28",
            "category": None
        },
        {
            "id": 2,
            "name": "Холодильник Indesit",
            "category_id": 4,
            "stock_quantity": 4,
            "price": 26799,
            "create_date": "2025-09-09T06:35:28",
            "category": None
        }
    ]
)
