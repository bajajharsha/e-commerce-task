from typing import List

from fastapi import Depends
from fastapi.responses import JSONResponse

from app.models.schemas.cart_schema import CartCreate, Order, OrderItem
from app.models.schemas.response_schema import BaseResponse
from app.repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, cart_repo: CartRepository = Depends(CartRepository)):
        self.cart_repo = cart_repo

    async def add_cart(
        self, cart_data: CartCreate, user_id
    ) -> BaseResponse:  # Return BaseResponse instead of UserResponse
        data = cart_data.dict()
        data["user_id"] = user_id

        if data["product_id"] == "" or data["product_id"] == None:
            return JSONResponse(
                status_code=400, content={"message": "Product ID is required"}
            )

        print(data)
        result = await self.cart_repo.add_cart(data)
        data["_id"] = str(result.inserted_id)
        return {"status": "success", "data": data}

    async def get_cart(self, user_id: str) -> BaseResponse:
        cart_items = await self.cart_repo.get_cart_by_user_id(user_id)
        if not cart_items:
            return {"status": "error", "message": "No cart items found for the user"}
        return {"status": "success", "data": cart_items, "count": len(cart_items)}

    async def place_order(self, user_id: str):
        # Fetch all cart items for the user
        cart_items = await self.cart_repo.get_cart_by_user_id(user_id)

        if not cart_items["data"]:
            return JSONResponse(
                status_code=400, content={"message": "Your cart is empty"}
            )

        order_items: List[OrderItem] = []
        total_amount = 0

        # Iterate over the cart items to create order items
        for item in cart_items["data"]:
            product_id = item["product_id"]
            quantity = item["quantity"]

            # Fetch product price by product_id
            product = await self.product_repo.get_product_by_id(product_id)

            if not product:
                return JSONResponse(
                    status_code=404,
                    content={"message": f"Product with ID {product_id} not found"},
                )

            price = product["price"]
            total_item_price = price * quantity
            order_items.append(
                OrderItem(
                    product_id=product_id, quantity=quantity, price=total_item_price
                )
            )
            total_amount += total_item_price

        # Create order schema object
        order = Order(
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            status="delivered",  # default status
        )

        # Insert order into the database
        result = await self.order_repo.create_order(order)

        # If order is placed successfully, empty the user's cart
        await self.cart_repo.clear_cart(user_id)

        return {
            "status": "success",
            "order_id": str(result.inserted_id),
            "total_amount": total_amount,
        }
