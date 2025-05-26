from fastapi import APIRouter, HTTPException
from app.models import IndustrialProduction, AirEmission, Wastewater
from app.database import engine

router = APIRouter()
collection_map = {
    "industrial": IndustrialProduction,
    "emissions": AirEmission,
    "wastewater": Wastewater
}

@router.post("/{collection_name}/")
async def add_data(collection_name: str, data: dict):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")
    instance = Model(**data)
    await engine.save(instance)
    return instance

@router.get("/{collection_name}/")
async def get_data(collection_name: str):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")
    return await engine.find(Model)
