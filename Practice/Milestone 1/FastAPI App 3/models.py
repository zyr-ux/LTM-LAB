from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class GymBranches(Base):

    __tablename__ = 'gym_branches'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    city = Column(String,nullable=False)

    membership_plan = relationship('MembershipPlan',back_populates='gym_branch')

class MembershipPlan(Base):

    __tablename__ = 'membership_plans'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    duration_months = Column(Integer,nullable=False)
    monthly_fee = Column(Integer,nullable=False)
    guest_passes = Column(Integer,nullable=False)
    branch_id = Column(Integer,ForeignKey('gym_branches.id'),nullable=False)

    gym_branch = relationship('GymBranches',back_populates='membership_plan')
