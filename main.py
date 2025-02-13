from fastapi import FastAPI

from app.routes import (
    auth_routes,
    cart_route,
    complaint_route,
    order_route,
    products_route,
)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(products_route.router)
app.include_router(complaint_route.router)
app.include_router(cart_route.router)
app.include_router(order_route.router)
