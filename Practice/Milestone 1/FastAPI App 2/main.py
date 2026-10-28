from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models, schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/skill-groups',
        response_model=schemas.SkillGroupOut,
        status_code=201)
def create_skill_group(skill_group_data:schemas.SkillGroupCreate,
                    db : Session = Depends(get_db)):

    new_skill_group = models.SkillGroup(
        name = skill_group_data.name,
        floor_number = skill_group_data.floor_number
    )

    db.add(new_skill_group)
    db.commit()
    db.refresh(new_skill_group)

    return new_skill_group

app.post('/skill-groups/{parent_id}/trainers',
        response_model=schemas.TrainerOut,
        status_code=201)
def create_trainer(parent_id:int,
                    trainer_data:schemas.TrainersCreate,
                    db : Session = Depends(get_db)):

    skill_group = db.query(models.SkillGroup).filter(models.SkillGroup.id == parent_id).first()

    if skill_group is None:
        raise HTTPException(status_code=404,detail='skill_group not found')

    new_trainer = models.Trainer(
        name = trainer_data.name,
        designation = trainer_data.designation,
        session_fee = trainer_data.session_fee,
        experience_years = trainer_data.experience_years,
        skill_group = parent_id
    )

    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)

    return new_trainer

@app.put('/skill-groups/{parent_id}/trainers/{child_id}',
        response_model=schemas.TrainerOut, status_code=200)
def update_trainer(parent_id : int, child_id : int, trainer_input_data:schemas.TrainersCreate,
                    db : Session = Depends(get_db)):
    skill_group_data = db.query(models.SkillGroup).filter(models.SkillGroup.id == parent_id).first()
    if not skill_group_data:
        raise HTTPException(404,'skill group not found')

    trainer_data = db.query(models.Trainer).filter(models.Trainer.id == child_id).first()
    if not trainer_data:
        raise HTTPException(404,'trainer not found')

    if trainer_data.skillgroup_id != parent_id:
        raise HTTPException(404,'Foreign key not found')

    trainer_data.id = child_id
    trainer_data.name = trainer_input_data.name
    trainer_data.designation = trainer_input_data.designation
    trainer_data.session_fee = trainer_input_data.session_fee
    trainer_data.experience_years = trainer_input_data.experience_years
    trainer_data.skillgroup_id = parent_id

    db.commit()
    db.refresh(trainer_data)

    return trainer_data

@app.get('/skill-groups/{parent_id}',response_model=schemas.SkillGroupWithTrainers,status_code=200)
def get_skill_groups_with_trainers(parent_id : int, sort : str | None = None, designation : str | None = None,
                                    db : Session = Depends(get_db)):
        
        skill_group_data = db.query(models.SkillGroup).filter(models.SkillGroup.id == parent_id).first()

        if not skill_group_data:
            raise HTTPException(404,'skill group not found')

        if sort is not None:
            if sort != 'name' and sort != 'session_fee':
                raise HTTPException(404,'invalid sort parameter')

        trainer_query = db.query(models.Trainer).filter(models.Trainer.skillgroup_id == parent_id)

        if designation is not None:
            if designation.strip() != '':
                designation = designation.strip()
                trainer_query = trainer_query.filter(models.Trainer.designation == designation)

        if sort == 'name':
            trainer_query = trainer_query.order_by(models.Trainer.name.asc())

        if sort == 'session_fee':
            trainer_query = trainer_query.order_by(models.Trainer.session_fee.asc())

        trainers = trainer_query.all()

        response = {
            'id' : parent_id,
            'name' : skill_group_data.name,
            'floor_number' : skill_group_data.floor_number,
            'trainers' : trainers
        }

        return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host='localhost',port=8000,reload=True)

