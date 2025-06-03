from fastapi import APIRouter
from app.models import IndustrialProduction, AirEmission
from app.database import engine
import numpy as np

router = APIRouter()

@router.get("/correlation")
async def calculate_correlation():
    industrial = await engine.find(IndustrialProduction)
    emissions = await engine.find(AirEmission)

    prod_by_year = {}
    for record in industrial:
        year = record.year
        prod_by_year[year] = prod_by_year.get(year, 0) + record.value_mln_pln

    emis_by_year = {}
    for record in emissions:
        year = record.year
        emis_by_year[year] = emis_by_year.get(year, 0) + record.amount_tonnes

    common_years = set(prod_by_year.keys()) & set(emis_by_year.keys())
    if len(common_years) < 2:
        return {"message": "Za mało wspólnych lat, aby policzyć korelację."}

    prod_values = [prod_by_year[year] for year in sorted(common_years)]
    emis_values = [emis_by_year[year] for year in sorted(common_years)]

    correlation = np.corrcoef(prod_values, emis_values)[0][1]

    return {
        "common_years": sorted(common_years),
        "correlation": round(float(correlation), 3),
        "meaning": interpret_correlation(correlation)
    }

def interpret_correlation(corr):
    abs_corr = abs(corr)
    if abs_corr >= 0.9:
        return "bardzo silna zależność"
    elif abs_corr >= 0.7:
        return "silna zależność"
    elif abs_corr >= 0.5:
        return "umiarkowana zależność"
    elif abs_corr >= 0.3:
        return "słaba zależność"
    else:
        return "brak lub bardzo słaba zależność"
