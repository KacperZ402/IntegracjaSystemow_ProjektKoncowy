from fastapi import APIRouter, HTTPException, Query
from app.models import IndustrialProduction, AirEmission, Wastewater
from app.database import engine

router = APIRouter()

@router.get("/report")
async def generate_report(year: int = Query(..., ge=1900, le=2100)):
    industrial = await engine.find(IndustrialProduction, IndustrialProduction.year == year)
    emissions = await engine.find(AirEmission, AirEmission.year == year)
    wastewater = await engine.find(Wastewater, Wastewater.year == year)

    industrial_data = [i.dict(exclude={"id"}) for i in industrial]
    emissions_data = [e.dict(exclude={"id"}) for e in emissions]
    wastewater_data = [w.dict(exclude={"id"}) for w in wastewater]


    report = {
        "year": year,
        "summary": {
            "industrial_total_mln_pln": sum(i["value_mln_pln"] for i in industrial_data),
            "emissions_total_tonnes": sum(e["amount_tonnes"] for e in emissions_data),
            "wastewater_total_hm3": sum(w["volume_hm3"] for w in wastewater_data),
        },
        "details": {
            "industrial": industrial_data,
            "emissions": emissions_data,
            "wastewater": wastewater_data,
        }
    }

    return report
