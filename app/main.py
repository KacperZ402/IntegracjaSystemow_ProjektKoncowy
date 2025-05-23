from fastapi import FastAPI
from app.routes import entries
from app.database import connect_to_mongo

app = FastAPI(title="EcoIndustry API")

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

app.include_router(entries.router)
