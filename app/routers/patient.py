"""Patient API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get("", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    """Retrieve all patients."""
    statement = select(Patient)
    return db.scalars(statement).all()


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):
    """Create a new patient."""
    existing_patient = db.scalar(
        select(Patient).where(Patient.email == patient.email)
    )

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient with this email already exists",
        )

    new_patient = Patient(
        name=patient.name,
        email=patient.email,
        phone=patient.phone,
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a patient by ID."""
    patient = db.get(Patient, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return patient
