"""Pydantic schemas package."""

from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.schemas.patient import PatientCreate, PatientResponse

__all__ = [
    "PatientCreate",
    "PatientResponse",
    "DoctorCreate",
    "DoctorResponse",
    "AppointmentCreate",
    "AppointmentResponse",
]
