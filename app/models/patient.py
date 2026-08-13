"""Patient database model."""
# pylint: disable=too-few-public-methods


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Patient(Base):
    """Represent a patient in the database."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="patient",
    )
