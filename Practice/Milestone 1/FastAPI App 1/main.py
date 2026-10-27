from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models, schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/practice-areas',
        response_model=schemas.PracticeAreaOut,
        status_code=201)
def create_practice_area(practice_area: schemas.PracticeAreaCreate,
                        db:Session = Depends(get_db)):

    new_practice_area = models.PracticeArea(
        name = practice_area.name,
        floor_number = practice_area.floor_number
    )

    db.add(new_practice_area)
    db.commit()
    db.refresh(new_practice_area)

    return new_practice_area

@app.post('/practice-areas/{parent_id}/consultants',
        response_model=schemas.ConsultantOut,
        status_code=201)
def create_consultant(parent_id :int,
                    consultant : schemas.ConsultantCreate,
                    db: Session = Depends(get_db)):
    practice_area = db.query(models.PracticeArea).filter(models.PracticeArea.id == parent_id).first()

    if practice_area is None:
        raise HTTPException(status_code=404,detail='P not found')

    new_consultant = models.Consultant(
            name = consultant.name,
            designation = consultant.designation,
            consultaion_fees = consultant.consultation_fee,
            esperience_years = consultant.experience_years
    )

    db.add(new_consultant)
    db.commit()
    db.refresh(new_consultant)

    return new_consultant

@app.put('/practice-areas/{parent_id}/consultants/{child_id}',
        response_model=schemas.ConsultantOut,
        status_code=200)
def update_consultant(parent_id :int,child_id:int,
                    consultant_data:schemas.ConsultantCreate,
                    db : Session = Depends(get_db)):
    
    practice_area = db.query(models.PracticeArea).filter(models.PracticeArea.id == parent_id).first()
    if practice_area is None:
        raise HTTPException(status_code=404,detail='ID not found')

    consultant = db.query(models.Consultant).filter(models.Consultant.id == child_id,models.Consultant.practicearea_id == parent_id).first()

    if consultant is None:
        raise HTTPException(status_code=404,detail='Consultant doesnt exist')

    consultant.name = consultant_data.name
    consultant.designation = consultant_data.designation
    consultant.consultation_fee = consultant_data.consultation_fee
    consultant.experience_years = consultant_data.experience_years

    db.commit()
    db.refresh(consultant)

    return consultant


@app.get('/practice_areas',
        response_model=list[schemas.PracticeAreaWithConsultants],
        status_code=200)
def practice_areas_with_consultants(db : Session = Depends(get_db)):
    practice_areas_with_consultants_data = db.query(models.PracticeArea).all()
    return practice_areas_with_consultants_data

@app.get(
    "/practice-areas/{parent_id}",
    response_model=schemas.PracticeAreaWithConsultants,
    status_code=200
)
def get_practice_area(
    parent_id: int,
    designation: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    practice_area = (
        db.query(models.PracticeArea)
        .filter(models.PracticeArea.id == parent_id)
        .first()
    )

    if practice_area is None:
        raise HTTPException(
            status_code=404,
            detail="Practice area not found"
        )

    if sort is not None:
        if sort != "name" and sort != "consultation_fee":
            raise HTTPException(
                status_code=404,
                detail="Invalid sort parameter"
            )

    consultants_query = (
        db.query(models.Consultant)
        .filter(models.Consultant.practicearea_id == parent_id)
    )

    if designation is not None:
        if designation.strip() != "":
            consultants_query = consultants_query.filter(
                models.Consultant.designation == designation
            )

    if sort == "name":
        consultants_query = consultants_query.order_by(
            models.Consultant.name.asc()
        )

    if sort == "consultation_fee":
        consultants_query = consultants_query.order_by(
            models.Consultant.consultation_fee.asc()
        )

    consultants = consultants_query.all()

    response = {
        "id": practice_area.id,
        "name": practice_area.name,
        "floor_number": practice_area.floor_number,
        "consultants": consultants
    }

    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app',host='localhost',port=8000,reload=True)