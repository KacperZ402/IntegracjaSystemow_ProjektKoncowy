from pydantic import BaseModel

class IndustrialProductionBase(BaseModel):
    year: int
    sector: str
    value_mln_pln: float

class IndustrialProductionCreate(IndustrialProductionBase):
    pass

class IndustrialProductionOut(IndustrialProductionBase):
    id: int
    class Config:
        orm_mode = True


class AirEmissionBase(BaseModel):
    year: int
    pollutant: str
    amount_tonnes: float

class AirEmissionCreate(AirEmissionBase):
    pass

class AirEmissionOut(AirEmissionBase):
    id: int
    class Config:
        orm_mode = True


class WastewaterBase(BaseModel):
    year: int
    category: str
    volume_hm3: float

class WastewaterCreate(WastewaterBase):
    pass

class WastewaterOut(WastewaterBase):
    id: int
    class Config:
        orm_mode = True
