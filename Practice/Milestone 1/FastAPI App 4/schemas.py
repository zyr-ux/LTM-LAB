from pydantic import BaseModel, ConfigDict, Field, field_validator


class FarmCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra="forbid")

    name: str = Field(min_length=1)
    region: str = Field(min_length=1)

    @field_validator("name", "region")
    @classmethod
    def check_non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return value


class FarmOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    region: str


class CropBatchCreate(BaseModel):

    model_config = ConfigDict(strict=True,extra="forbid")

    batch_name: str = Field(min_length=1)
    crop_type: str = Field(min_length=1)
    expected_yield_kg: int = Field(ge=0)
    area_hectares: int = Field(ge=1)

    @field_validator("batch_name", "crop_type")
    @classmethod
    def check_non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return value


class CropBatchOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    batch_name: str
    crop_type: str
    expected_yield_kg: int
    area_hectares: int


class FarmWithChildren(FarmOut):

    model_config = ConfigDict(from_attributes=True)

    crop_batches: list[CropBatchOut]