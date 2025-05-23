from fastapi import APIRouter
from app.models import IndustryEntry
from app.database import db

router = APIRouter()

@router.post("/add-entry")
async def add_entry(entry: IndustryEntry):
    result = await db.entries.insert_one(entry.dict())
    return {"id": str(result.inserted_id)}

@router.get("/entries")
async def list_entries():
    entries = await db.entries.find().to_list(100)
    return entries
