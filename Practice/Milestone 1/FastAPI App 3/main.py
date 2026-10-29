from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import uvicorn
import models, schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/branches',
        response_model=schemas.BranchOut,
        status_code=201)
def create_branch(input_branch_data : schemas.BranchCreate,
                  db : Session = Depends(get_db)):

    new_branch_data = models.GymBranches(
        name = input_branch_data.name,
        city = input_branch_data.city
    )

    db.add(new_branch_data)
    db.commit()
    db.refresh(new_branch_data)

    return new_branch_data

@app.post('/branches/{parent_id}/membership_plans',
          response_model=schemas.MembershipPlanOut,
          status_code=201)
def create_membership_plan(parent_id:int,
                           input_membership_plan_data:schemas.MembershipPlanCreate,
                           db : Session = Depends(get_db)):
    branch_data = db.query(models.GymBranches).filter(models.GymBranches.id == parent_id).first()

    if not branch_data:
        raise HTTPException(404,'Gym Branch not found')

    new_membership_plan = models.MembershipPlan(
        name = input_membership_plan_data.name,
        duration_months = input_membership_plan_data.duration_months,
        monthly_fee = input_membership_plan_data.monthly_fee,
        guest_passes = input_membership_plan_data.guest_passes,
        branch_id = parent_id
    )
    db.add(new_membership_plan)
    db.commit()
    db.refresh(new_membership_plan)

    return new_membership_plan

@app.put('/branches/{parent_id}/membership_plans/{child_id}',
         response_model=schemas.MembershipPlanOut,
         status_code=200)
def update_membership_plan(parent_id : int, child_id : int,
                           input_membership_plan_data : schemas.MembershipPlanCreate,
                           db : Session = Depends(get_db)):
    
    # membership_plan_data = db.query(models.MembershipPlan).filter(models.MembershipPlan.id == child_id, models.MembershipPlan.branch_id == parent_id).first()

    branches_data = db.query(models.GymBranches).filter(models.GymBranches.id == parent_id).first()

    if not branches_data:
        raise HTTPException(404,'Gym Branch not found')

    membership_plan_data = db.query(models.MembershipPlan).filter(models.MembershipPlan.id == child_id).first()

    if not membership_plan_data:
        raise HTTPException(404,'Membership Plan not found')

    if membership_plan_data.branch_id != parent_id:
        raise HTTPException(404, 'Membership Plan has invalid Branch ID')

    membership_plan_data.name = input_membership_plan_data.name
    membership_plan_data.duration_months = input_membership_plan_data.duration_months
    membership_plan_data.monthly_fee = input_membership_plan_data.monthly_fee
    membership_plan_data.guest_passes = input_membership_plan_data.guest_passes

    db.commit()
    db.refresh(membership_plan_data)

    return membership_plan_data

@app.get('/branches/{parent_id}',response_model=schemas.BranchWithPlans,status_code=200)
def get_branches_with_plans(parent_id : int, duration_months : str | None = None, sort : str | None = None,
                            db : Session = Depends(get_db)):

    branch_data = db.query(models.GymBranches).filter(models.GymBranches.id == parent_id).first()

    if not branch_data:
        raise HTTPException(404,'Gym Branch not found')

    if sort is not None:
        if sort != 'name' and sort != 'monthly_fee':
            raise HTTPException(404, 'Invalid sort parameter')

    membership_plan_query = db.query(models.MembershipPlan).filter(models.MembershipPlan.branch_id == parent_id)

    if duration_months is not None and duration_months.strip() != '':
        duration_months : int = int(duration_months)
        if duration_months > 0:
            membership_plan_query = membership_plan_query.filter(models.MembershipPlan.duration_months == duration_months)

    if sort == 'name':
        membership_plan_query = membership_plan_query.order_by(models.MembershipPlan.name.asc(),models.MembershipPlan.id.asc())

    if sort == 'monthly_fee':
        membership_plan_query = membership_plan_query.order_by(models.MembershipPlan.monthly_fee.asc(),models.MembershipPlan.id.asc())

    if not sort:
        membership_plan_query = membership_plan_query.order_by(models.MembershipPlan.id.asc()) 

    membership_plan_data = membership_plan_query.all()

    response = {
        'id' : branch_data.id,
        'name' : branch_data.name,
        'city' : branch_data.city,
        'membership_plans' : membership_plan_data
    }

    return response

if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8080,reload=True)

