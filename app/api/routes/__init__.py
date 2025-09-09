from fastapi import APIRouter, Depends

from app.api.dependencies.auth import check_api_key
from app.api.routes import (
    client,
    order,
    product,
)


def setup() -> APIRouter:
    router = APIRouter(
        dependencies=[Depends(check_api_key)]
    )
    router.include_router(client.setup())
    router.include_router(product.setup())
    router.include_router(order.setup())
    return router
