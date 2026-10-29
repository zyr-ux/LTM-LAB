from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import uvicorn
import models, schemas
from database import Base, engine, get_db

app = FastAPI()

@app.post('/farms',response_model=schemas.FarmOut,status_code=201)
def create_farm(input_farm_data:schemas.FarmCreate,db : Session = Depends(get_db)):

    new_farm_data = models.Farms(
        name = input_farm_data.name,
        region = input_farm_data.region
    )

    db.add(new_farm_data)
    db.commit()
    db.refresh(new_farm_data)

    return new_farm_data

@app.post('/farms/{parent_id}/crop_batches',response_model=schemas.CropBatchOut,status_code=201)
def create_crop_batch(parent_id : int,input_crop_data:schemas.CropBatchCreate,db : Session = Depends(get_db)):

    farm_data = db.query(models.Farms).filter(models.Farms.id == parent_id).first()

    if not farm_data:
        raise HTTPException(404,'not found')

    new_farm_data = models.Farms(
        batch_name = input_crop_data.batch_name,
        crop_type = input_crop_data.crop_type,
        expected_yield_kg = input_crop_data.expected_yield_kg,
        area_hectares = input_crop_data.area_hectares,
        farm_id = parent_id
    )

    db.add(new_farm_data)
    db.commit()
    db.refresh(new_farm_data)

    return new_farm_data