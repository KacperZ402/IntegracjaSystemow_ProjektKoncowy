from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.database import engine
from app.models import IndustrialProduction, AirEmission, Wastewater
import matplotlib.pyplot as plt
import pandas as pd

router = APIRouter()

@router.get("/charts/{kind}")
async def generate_chart(kind: str):
    if kind == "industrial":
        records = await engine.find(IndustrialProduction)
        df = pd.DataFrame([r.dict(exclude={"id"}) for r in records])
        df = df.groupby("year")["value_mln_pln"].sum().reset_index()
        ylabel = "mln PLN"
        title = "Produkcja przemysłowa"
    elif kind == "emissions":
        records = await engine.find(AirEmission)
        df = pd.DataFrame([r.dict(exclude={"id"}) for r in records])
        df = df.groupby("year")["amount_tonnes"].sum().reset_index()
        ylabel = "tony"
        title = "Emisja zanieczyszczeń"
    elif kind == "wastewater":
        records = await engine.find(Wastewater)
        df = pd.DataFrame([r.dict(exclude={"id"}) for r in records])
        df = df.groupby("year")["volume_hm3"].sum().reset_index()
        ylabel = "hm³"
        title = "Ścieki odprowadzane"
    else:
        return {"error": "Nieznany typ wykresu"}

    plt.figure()
    plt.plot(df["year"], df.iloc[:, 1], marker='o')
    plt.title(title)
    plt.xlabel("Rok")
    plt.ylabel(ylabel)
    plt.grid(True)

    path = f"frontend/wykres_{kind}.png"
    plt.savefig(path)
    plt.close()
    return FileResponse(path, media_type="image/png")
