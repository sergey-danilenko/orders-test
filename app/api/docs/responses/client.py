from app.api.utils.response_factory import ResponseFactory

factory = ResponseFactory()

CLIENT_LIST = factory.ok(
    example=
    [
        {
            "id": 1,
            "name": "ИП Компания № 1",
            "create_date": "2025-09-09T06:35:28",
            "address": "Москва, ул. Трофимова, 32к1",
            "orders": None
        },
        {
            "id": 2,
            "name": "ООО Компания № 2",
            "create_date": "2025-09-09T06:35:28",
            "address": "Москва, ул. Каширское шоссе, 4к3",
            "orders": None
        }
    ]
)
