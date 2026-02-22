from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.appointment import Appointment


def list_appointments(db: Session, from_date: date | None = None, to_date: date | None = None):
    q = select(Appointment).order_by(Appointment.date, Appointment.time)
    if from_date is not None:
        q = q.where(Appointment.date >= from_date)
    if to_date is not None:
        q = q.where(Appointment.date <= to_date)
    return db.execute(q).scalars().all()


def get_today_appointments(db: Session, today: date):
    return list_appointments(db, from_date=today, to_date=today)


def get_upcoming_appointments(db: Session, after_date: date):
    return list_appointments(db, from_date=after_date)


def get_appointment_by_id(db: Session, appointment_id: int) -> Appointment | None:
    return db.get(Appointment, appointment_id)


def create_appointment(
    db: Session, customer_id: int, date: date, time: time, notes: str = "", status: str = "Scheduled"
) -> Appointment:
    apt = Appointment(customer_id=customer_id, date=date, time=time, notes=notes, status=status)
    db.add(apt)
    db.commit()
    db.refresh(apt)
    return apt


def update_appointment(
    db: Session,
    appointment: Appointment,
    date: date | None = None,
    time: time | None = None,
    notes: str | None = None,
    status: str | None = None,
) -> Appointment:
    if date is not None:
        appointment.date = date
    if time is not None:
        appointment.time = time
    if notes is not None:
        appointment.notes = notes
    if status is not None:
        appointment.status = status
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment: Appointment) -> None:
    db.delete(appointment)
    db.commit()


def mark_completed(db: Session, appointment: Appointment) -> Appointment:
    appointment.status = "Completed"
    db.commit()
    db.refresh(appointment)
    return appointment
