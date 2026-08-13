"""Database models package."""

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient

__all__ = ["Patient", "Doctor", "Appointment"]
