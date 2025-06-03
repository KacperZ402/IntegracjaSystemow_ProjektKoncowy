import json
import asyncio
from odmantic import AIOEngine, Model
from motor.motor_asyncio import AsyncIOMotorClient

# === MODELE ===
class IndustrialProduction(Model):
    year: int
    sector: str
    value_mln_pln: float

class AirEmission(Model):
    year: int
    pollutant: str
    amount_tonnes: float

class Wastewater(Model):
    year: int
    category: str
    volume_hm3: float

# === KONFIGURACJA BAZY ===
MONGO_URI = "mongodb+srv://admin:admin@cluster0.7fugtco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
engine = AIOEngine(client, database="integracja")

# === FUNKCJE IMPORTUJĄCE ===
async def import_data():
    with open("dane_przemyslowe.json", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            await engine.save(IndustrialProduction(**entry))

    with open("dane_sciekowe.json", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            await engine.save(Wastewater(**entry))

    with open("dane_emisje.json", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            await engine.save(AirEmission(**entry))

# === URUCHOMIENIE ===
if __name__ == "__main__":
    asyncio.run(import_data())
