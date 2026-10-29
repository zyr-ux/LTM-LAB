from pydantic import BaseModel, Field, ConfigDict, field_validator

class BranchCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    name : str = Field(min_length=1)
    city : str = Field(min_length=1)

    @field_validator('name')
    @classmethod
    def check_name(cls,value):
        if not value.strip():
            raise ValueError('Name cannot be empty')
        return value

    @field_validator('city')
    @classmethod
    def check_city(cls,value):
        if not value.strip():
            raise ValueError('City cannot be empty')
        return value

class BranchOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    city : str

class MembershipPlanCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    name : str = Field(min_length=1)
    duration_months : int = Field(ge=1)
    monthly_fee : int = Field(ge=300)
    guest_passes : int = Field(ge=0)

    @field_validator('name')
    @classmethod
    def check_name(cls,value):
        if not value.strip():
            raise ValueError('Name cannot be empty')
        return value

class MembershipPlanOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    duration_months : int
    monthly_fee : int
    guest_passes : int

class BranchWithPlans(BranchOut):

    model_config = ConfigDict(from_attributes=True)

    membership_plans : list[MembershipPlanOut]