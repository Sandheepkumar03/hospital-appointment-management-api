"""Pydantic schemas for patients."""

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    """Common patient fields."""

    name: str
    email: str
    phone: str


class PatientCreate(PatientBase):
    """Schema for creating a patient."""


class PatientResponse(PatientBase):
    """Schema returned when retrieving a patient."""

    id: int

    model_config = ConfigDict(from_attributes=True)
