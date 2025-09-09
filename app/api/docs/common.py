from app.api.utils.response_factory import ResponseFactory

factory = ResponseFactory()

UNAUTHORIZED_ERROR = factory.unauthorized()

VALIDATION_ERROR = factory.unprocessable_entity(
    detail=[
        {
            "loc": [
                "string",
                0
            ],
            "msg": "string",
            "type": "string"
        }
    ]
)
