from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IndustryEntry(BaseModel):
    year: int
    region: str
    industry_value: float
    co2_emissions: float
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
