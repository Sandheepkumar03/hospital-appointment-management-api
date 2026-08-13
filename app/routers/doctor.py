"""Doctor API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.get("", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    """Retrieve all doctors."""
    statement = select(Doctor)
    return db.scalars(statement).all()


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    """Create a new doctor."""
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a doctor by ID."""
    doctor = db.get(Doctor, doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    return doctor
