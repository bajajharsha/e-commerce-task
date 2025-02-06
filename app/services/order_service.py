from app.repositories.cart_repository import CartRepository
from app.repositories.products_repository import ProductsRepository  # Assuming you have a product repo
from app.repositories.order_repository import OrderRepository
from app.models.schemas.cart_schema import Order, OrderItem
from app.models.schemas.response_schema import BaseResponse
from fastapi.responses import JSONResponse
from typing import List
from fastapi import Depends

class OrderService:
    def __init__(self, cart_repo: CartRepository = Depends(CartRepository),
                 product_repo: ProductsRepository = Depends(ProductsRepository),
                 order_repo: OrderRepository = Depends(OrderRepository)):
        self.cart_repo = cart_repo
        self.product_repo = product_repo
        self.order_repo = order_repo

    async def place_order(self, user_id: str) -> BaseResponse:
        # Fetch all cart items for the user
        cart_items = await self.cart_repo.get_cart_by_user_id(user_id)

        if not cart_items:
            return JSONResponse(status_code=400, content={"message": "Your cart is empty"})

        order_items: List[OrderItem] = []
        total_amount = 0

        # Iterate over the cart items to create order items
        for item in cart_items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            # Fetch product price by product_id
            product = await self.product_repo.get_product_by_id(product_id)

            if not product:
                return JSONResponse(status_code=404, content={"message": f"Product with ID {product_id} not found"})

            price = product["price"]
            total_item_price = price * quantity
            order_items.append(OrderItem(product_id=product_id, quantity=quantity, price=total_item_price))
            total_amount += total_item_price

        # Create order schema object
        order = Order(
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            status="delivered"  # default status
        )

        # Insert order into the database
        result = await self.order_repo.create_order(order)

        # If order is placed successfully, empty the user's cart
        await self.cart_repo.clear_cart(user_id)

        return {
            "status": "success",
            "order_id": str(result.inserted_id),
            "total_amount": total_amount,
            "order_items": order_items
        }
