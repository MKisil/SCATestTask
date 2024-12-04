from pydantic import BaseModel, field_validator, ConfigDict


class SpyCatCreateScheme(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: int

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 255:
            raise ValueError('Field "name" must be at most 255 characters.')
        return v

    @field_validator('years_experience')
    def validate_years_experience(cls, v):
        if v < 0 or v > 50:
            raise ValueError('Field "years_experience" must be between 0 and 50.')
        return v

    @field_validator('salary')
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Field "salary" must be greater than 0.')
        return v

    @field_validator('breed')
    def validate_breed(cls, v):
        if len(v) > 4:
            raise ValueError('Field "breed" must be at most 4 characters.')
        return v

    model_config = ConfigDict(from_attributes=True)


class SpyCatGetScheme(BaseModel):
    id: int
    name: str
    years_experience: int
    breed: str
    salary: int

    model_config = ConfigDict(from_attributes=True)


class SpyCatUpdateSalaryScheme(BaseModel):
    id: int
    salary: int

    @field_validator('salary')
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Field "salary" must be greater than 0.')
        return v

