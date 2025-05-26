from odmantic import Model
from typing import Optional

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
