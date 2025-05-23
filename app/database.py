import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.ecoindustry

async def connect_to_mongo():
    try:
        await client.admin.command('ping')
        print("✅ Połączono z MongoDB")
    except Exception as e:
        print("❌ Błąd połączenia z MongoDB:", e)
