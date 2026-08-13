"""Pydantic schemas for appointments."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    """Common appointment fields."""

    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime


class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment."""


class AppointmentResponse(AppointmentBase):
    """Schema returned when retrieving an appointment."""

    id: int

    model_config = ConfigDict(from_attributes=True)
