"""Appointment API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse


router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


@router.get("", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    """Retrieve all appointments."""
    statement = select(Appointment)
    return db.scalars(statement).all()


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new appointment."""

    patient = db.get(Patient, appointment.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    doctor = db.get(Doctor, appointment.doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    overlapping_appointment = db.scalar(
        select(Appointment).where(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_start < appointment.appointment_end,
            Appointment.appointment_end > appointment.appointment_start,
        )
    )

    if overlapping_appointment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already has an appointment during this time",
        )


    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_start=appointment.appointment_start,
        appointment_end=appointment.appointment_end,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve an appointment by ID."""

    appointment = db.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    return appointment
