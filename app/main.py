"""Main FastAPI application."""

from fastapi import FastAPI

from app.routers.patient import router as patient_router
from app.routers.doctor import router as doctor_router
from app.routers.appointment import router as appointment_router

app = FastAPI(
    title="Hospital Appointment Management API",
    version="1.0.0",
)

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


@app.get("/")
def root():
    """Return the API welcome message."""
    return {"message": "Hospital Appointment Management API"}
