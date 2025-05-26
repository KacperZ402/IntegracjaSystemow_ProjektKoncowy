from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import IndustrialProduction, AirEmission, Wastewater
import xml.etree.ElementTree as ET
import os
import json
import yaml  # <- nowość
from app.auth import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from datetime import timedelta


app = FastAPI()

# --- MODELE DO PRZETWARZANIA ---
collection_map = {
    "industrial": IndustrialProduction,
    "emissions": AirEmission,
    "wastewater": Wastewater
}


# --- ZAPIS DANYCH ---
@app.post("/{collection_name}/")
async def add_data(collection_name: str, data: dict):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")
    instance = Model(**data)
    await engine.save(instance)
    return instance


# --- ODCZYT DANYCH ---
@app.get("/{collection_name}/")
async def get_data(collection_name: str):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")
    return await engine.find(Model)


# --- POMOCNICZA FUNKCJA XML ---
def dict_list_to_xml(tag: str, items: list[dict]) -> str:
    root = ET.Element(tag)
    for item in items:
        entry = ET.SubElement(root, "entry")
        for key, val in item.items():
            if key != "_id":
                el = ET.SubElement(entry, key)
                el.text = str(val)
    return ET.tostring(root, encoding="utf-8", method="xml")


# --- EKSPORT DANYCH ---
@app.get("/export/{collection_name}")
async def export_data(
    collection_name: str,
    format: str = Query("json", enum=["json", "xml", "yaml"])
):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")

    records = await engine.find(Model)
    data = [r.dict() for r in records]

    if format == "json":
        return JSONResponse(content=data)
    elif format == "xml":
        xml_data = dict_list_to_xml(collection_name, data)
        return Response(content=xml_data, media_type="application/xml")
    elif format == "yaml":
        yaml_data = yaml.dump(data, allow_unicode=True)
        return Response(content=yaml_data, media_type="application/x-yaml")


# --- IMPORT DANYCH Z PLIKU ---
@app.post("/import/{collection_name}")
async def import_data(collection_name: str, file: UploadFile = File(...)):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")

    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".json"):
        data = json.loads(content)
    elif filename.endswith(".yaml") or filename.endswith(".yml"):
        data = yaml.safe_load(content)
    elif filename.endswith(".xml"):
        tree = ET.fromstring(content)
        data = []
        for entry in tree.findall("entry"):
            item = {child.tag: child.text for child in entry}
            data.append(item)
    else:
        raise HTTPException(status_code=400, detail="Nieobsługiwany format pliku")

    for record in data:
        instance = Model(**record)
        await engine.save(instance)

    return {"imported": len(data)}


# --- FRONTEND STATYCZNY ---
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join("frontend", "index.html"))

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Błędna nazwa użytkownika lub hasło")
    token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
