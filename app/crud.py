from sqlalchemy.orm import Session
import models, schemas

def create_industrial_production(db: Session, data: schemas.IndustrialProductionCreate):
    db_obj = models.IndustrialProduction(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_industrial_production(db: Session):
    return db.query(models.IndustrialProduction).all()

def create_air_emission(db: Session, data: schemas.AirEmissionCreate):
    db_obj = models.AirEmission(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_air_emission(db: Session):
    return db.query(models.AirEmission).all()

def create_wastewater(db: Session, data: schemas.WastewaterCreate):
    db_obj = models.Wastewater(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_wastewater(db: Session):
    return db.query(models.Wastewater).all()

