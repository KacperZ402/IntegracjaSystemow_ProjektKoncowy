import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Przykładowe zewnętrzne źródło danych (można zamienić na inne)
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/posts"

@router.get("/external/fetch")
async def fetch_external_data():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(EXTERNAL_API_URL)
            response.raise_for_status()
            data = response.json()
            return {
                "source": EXTERNAL_API_URL,
                "count": len(data),
                "sample": data[:3]  # pokazuje 3 przykładowe rekordy
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
