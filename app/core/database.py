from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = None
db = None

async def connect_db():#this function is  used to connect to the mongodb database and it will be called in the main.py
    global client,db

    client = AsyncIOMotorClient(settings.MONGODB_URL)#connect to mongodb using the url from the settings.py file
    db = client[settings.DATABASE_NAME]

    print(f"mongodb connect:{settings.DATABASE_NAME}")

async def disconnect_db():#this function is used to disconnect from the mongodb database and it will be called in the main.py
    global client
    if client:
        client.close()
        print("mongodb disconnect")

def get_db():#this function is used to get the database instance and it will be used in the api files to perform database operations
    return db