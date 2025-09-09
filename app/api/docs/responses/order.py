from app.api.utils.response_factory import ResponseFactory

factory = ResponseFactory()

ORDERS_LIST = factory.ok(
    example=[
      {
        "id": 7,
        "client_id": 3,
        "create_date": "2025-09-09T08:55:56"
      },
      {
        "id": 6,
        "client_id": 6,
        "create_date": "2025-09-09T06:35:28"
      }
    ]
)

CREATE_ORDER = factory.ok(
    example=
    {
        "id": 7,
        "client_id": 3,
        "create_date": "2025-09-09T08:55:56",
    }
)

UPDATE_ORDER = factory.ok(
    example=
    {
        "id": 7,
        "client_id": 3,
    }
)

BAD_REQUEST = factory.bad_request(
    detail="The product/s is out of stock or unavailable with: product_id = 25"
)
