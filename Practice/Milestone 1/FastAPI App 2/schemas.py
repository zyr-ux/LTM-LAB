from pydantic import BaseModel, Field, ConfigDict, field_validator

class SkillGroupCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    name : str = Field(min_length=1)
    floor_number : int = Field(ge=1)

    @field_validator('name')
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError('Name cannot be empty')
        return value

class SkillGroupOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    floor_number : int

class TrainersCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    name : str = Field(min_length=1)
    designation : str = Field(min_length=1)
    session_fee : int = Field(ge=300)
    experience_years : int = Field(ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError('Name cannot be emtpy')
        return value

    @field_validator('designation')
    @classmethod
    def validate_designtaion(cls,value):
        if not value.strip():
            raise ValueError('Designtaion cannot be empty')
        return value


class TrainerOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    desgination : str
    session_fee : int
    experience_years : int

class SkillGroupWithTrainers(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    floor_number : int
    trainers : list[TrainerOut]
