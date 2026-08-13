from fastapi.testclient import TestClient

from app.main import app as fastapi_app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import timezone


# Use an in-memory SQLite database for tests and override the app dependency
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import app.models  # ensure model modules are imported and registered with Base
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db
client = TestClient(fastapi_app)


def test_get_patients():
    response = client.get("/patients")
    assert response.status_code == 200


def test_get_doctors():
    response = client.get("/doctors")
    assert response.status_code == 200


def test_get_appointments():
    response = client.get("/appointments")
    assert response.status_code == 200


def test_get_patient_by_id():
    # create a patient then fetch by id
    payload = {"name": "Patient One", "email": "p1@example.com", "phone": "1111111111"}
    r = client.post("/patients", json=payload)
    assert r.status_code == 201
    pid = r.json()["id"]
    response = client.get(f"/patients/{pid}")
    assert response.status_code == 200


def test_get_doctor_by_id():
    # create a doctor then fetch by id
    payload = {"name": "Doctor One", "specialization": "Testing"}
    r = client.post("/doctors", json=payload)
    assert r.status_code == 201
    did = r.json()["id"]
    response = client.get(f"/doctors/{did}")
    assert response.status_code == 200


def test_get_appointment_by_id():
    # create patient and doctor, then an appointment and fetch by id
    p = client.post("/patients", json={"name": "A", "email": "a@example.com", "phone": "000"})
    assert p.status_code == 201
    pid = p.json()["id"]
    d = client.post("/doctors", json={"name": "D", "specialization": "S"})
    assert d.status_code == 201
    did = d.json()["id"]
    from datetime import datetime, timedelta
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=30)
    ap = client.post("/appointments", json={
        "patient_id": pid,
        "doctor_id": did,
        "appointment_start": start.isoformat(),
        "appointment_end": end.isoformat(),
    })
    assert ap.status_code == 201
    aid = ap.json()["id"]
    response = client.get(f"/appointments/{aid}")
    assert response.status_code == 200

def test_overlapping_appointment_rejected():
    import random
    from datetime import datetime, timedelta

    # Create unique patient for this test
    patient_payload = {
        "name": f"Test Patient {random.randint(1,10**9)}",
        "email": f"test-{random.randint(1,10**9)}@example.com",
        "phone": "0000000000",
    }
    p_res = client.post("/patients", json=patient_payload)
    assert p_res.status_code == 201
    patient_id = p_res.json()["id"]

    # Create unique doctor for this test
    doctor_payload = {
        "name": f"Test Doctor {random.randint(1,10**9)}",
        "specialization": "Testing",
    }
    d_res = client.post("/doctors", json=doctor_payload)
    assert d_res.status_code == 201
    doctor_id = d_res.json()["id"]

    start = datetime.now(timezone.utc) + timedelta(days=10000)
    end = start + timedelta(minutes=30)

    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_start": start.isoformat(),
        "appointment_end": end.isoformat(),
    }

    first_response = client.post("/appointments", json=payload)

    assert first_response.status_code == 201

    second_response = client.post("/appointments", json=payload)

    assert second_response.status_code == 409
