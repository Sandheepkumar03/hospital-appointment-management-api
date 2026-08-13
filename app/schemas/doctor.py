"""Pydantic schemas for doctors."""

from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    """Common doctor fields."""

    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    """Schema for creating a doctor."""


class DoctorResponse(DoctorBase):
    """Schema returned when retrieving a doctor."""

    id: int

    model_config = ConfigDict(from_attributes=True)
