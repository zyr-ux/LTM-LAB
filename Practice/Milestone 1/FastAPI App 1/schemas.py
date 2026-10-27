from pydantic import BaseModel, Field, ConfigDict, field_validator

class PracticeAreaCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')
    
    name : str = Field(min_length=1)
    floor_number : int = Field(ge=1)

class PracticeAreaOut(BaseModel):
    id : int
    name : str
    floor_number : int

    model_config = ConfigDict(from_attributes=True)

class ConsultantOut(BaseModel):
    id : int
    name : str
    designation : str
    consultation_fee : int
    experience_years : int

    model_config = ConfigDict(from_attributes=True)

class PracticeAreaWithConsultants(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    id : int
    name : str
    floor_number : int
    consultants : list[ConsultantOut]

    model_config = ConfigDict(from_attributes=True)

class ConsultantCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra='forbid')

    name : str = Field(min_length=1)
    designation : str = Field(min_length=1)
    consultation_fee : int = Field(ge=300)
    experience_years : int = Field(ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator('designation')
    @classmethod
    def validate_designation(cls,value):
        if not value.strip():
            raise ValueError("Designation must not be empty")
        return value