from typing import Union, Any

from fastapi import status

ExampleT = Union[dict[str, Any], list[dict[str, Any]], str] | None
ExamplesT = dict[str, dict[str, Any]] | None
DescriptionT = str | None
HeadersT = dict[str, Union[str, dict[str, str]]] | None


class ResponseFactory:
    def __init__(
        self,
        status_code: int = status.HTTP_200_OK,
        content_type: str = "application/json",
        description: DescriptionT = None,
        headers: HeadersT = None
    ):
        self.status_code = status_code
        self.content_type = content_type
        self.description = description
        self.headers = headers

    def create(
        self,
        status_code: int | None = None,
        content_type: str | None = None,
        example: ExampleT = None,
        examples: ExamplesT = None,
        description: DescriptionT = None,
        headers: HeadersT = None
    ) -> dict:
        if example and examples:
            raise ValueError(
                "Cannot use example and examples at the same time."
            )
        final_status_code = status_code or self.status_code
        final_content_type = content_type or self.content_type
        final_description = description or self.description
        final_headers = headers or self.headers

        content = {}

        if example:
            content[final_content_type] = {"example": example}
        elif examples:
            content[final_content_type] = {"examples": examples}
        else:
            content[final_content_type] = {}

        response_config = {
            final_status_code: {
                "content": content
            }
        }

        if final_description:
            response_config[final_status_code]["description"] = final_description

        if final_headers:
            formatted_headers = {}
            for key, value in final_headers.items():
                if isinstance(value, dict):
                    formatted_headers[key] = value
                else:
                    formatted_headers[key] = {"description": value}

            response_config[final_status_code]["headers"] = formatted_headers

        return response_config

    def empty(
        self,
        description: DescriptionT = None,
        headers: HeadersT = None
    ) -> dict:
        return self.create(description=description, headers=headers)

    def ok(
        self,
        content_type: str = "application/json",
        example: ExampleT = None,
        examples: ExamplesT = None,
        description: str = "Успешно"
    ) -> dict:
        return self.create(
            content_type=content_type,
            example=example,
            examples=examples,
            description=description
        )

    def not_ok(
        self,
        status_code: int,
        content_type: str = "application/json",
        description: str = "Неверный запрос",
        detail: ExampleT = "Invalid request",
    ) -> dict:
        return self.create(
            status_code=status_code,
            content_type=content_type,
            example={"detail": detail},
            description=description
        )

    def created(
        self,
        example: ExampleT = None,
        content_type: str = "application/json",
        description: str = "Ресурс создан"
    ) -> dict:
        return self.create(
            status_code=status.HTTP_201_CREATED,
            content_type=content_type,
            example=example,
            headers={"Location": "URL созданного ресурса"},
            description=description,
        )

    def unauthorized(
        self,
        content_type: str = "application/json",
        description: str = "Не авторизован",
        detail: ExampleT = "Invalid or missing API Key",
    ) -> dict:
        return self.create(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content_type=content_type,
            description=description,
            example={"detail": detail},
        )

    def not_found(
        self,
        content_type: str = "application/json",
        description: str = "Не найдено",
        detail: ExampleT = "Not found",
    ) -> dict:
        return self.create(
            status_code=status.HTTP_404_NOT_FOUND,
            content_type=content_type,
            description=description,
            example={"detail": detail}
        )

    def bad_request(
        self,
        content_type: str = "application/json",
        description: str = "Неверный запрос",
        detail: ExampleT = "Invalid request",
    ) -> dict:
        return self.create(
            status_code=status.HTTP_400_BAD_REQUEST,
            content_type=content_type,
            description=description,
            example={"detail": detail}
        )

    def unprocessable_entity(
        self,
        content_type: str = "application/json",
        description: str = "Ошибка валидации входных данных",
        detail: ExampleT = "Validation error",
    ) -> dict:
        return self.create(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content_type=content_type,
            description=description,
            example={"detail": detail}
        )
