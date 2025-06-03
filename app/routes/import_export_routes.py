from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends, Response
from fastapi.responses import JSONResponse
import xml.etree.ElementTree as ET
import json, yaml
from app.models import IndustrialProduction, AirEmission, Wastewater
from app.auth import get_current_user
from app.database import engine

router = APIRouter()
collection_map = {
    "industrial": IndustrialProduction,
    "emissions": AirEmission,
    "wastewater": Wastewater
}

def dict_list_to_xml(tag: str, items: list[dict]) -> str:
    root = ET.Element(tag)
    for item in items:
        entry = ET.SubElement(root, "entry")
        for key, val in item.items():
            if key != "_id":
                el = ET.SubElement(entry, key)
                el.text = str(val)
    return ET.tostring(root, encoding="utf-8", method="xml")

@router.get("/export/{collection_name}")
async def export_data(
    collection_name: str,
    format: str = Query("json", enum=["json", "xml", "yaml"]),
    user=Depends(get_current_user)
):
    Model = collection_map.get(collection_name)
    if not Model:
        raise HTTPException(status_code=404, detail="Nieznana kolekcja")

    records = await engine.find(Model)

    if format == "json":
        data = [r.dict(exclude={"id"}) for r in records]
        return JSONResponse(content=data)
    elif format == "xml":
        xml_data = dict_list_to_xml(collection_name, data)
        return Response(content=xml_data, media_type="application/xml")
    elif format == "yaml":
        yaml_data = yaml.dump(data, allow_unicode=True)
        return Response(content=yaml_data, media_type="application/x-yaml")

@router.post("/import/{collection_name}")
async def import_data(
    collection_name: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
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
