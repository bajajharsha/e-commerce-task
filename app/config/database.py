from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client[settings.mongodb_db]
        self.user_collection = self.db["users"]
        self.products_collection = self.db["products"]
        
    async def get_db(self):
        self.db

    def get_user_collection(self):
        return self.user_collection
    
    def get_products_collection(self):
        return self.products_collection

database = Database()


