from fastapi import FastAPI
from app.routes import auth_routes, products_route

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(products_route.router)
