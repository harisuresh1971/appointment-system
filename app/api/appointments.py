from datetime import date, time
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.appointment import (
    list_appointments,
    get_appointment_by_id,
    create_appointment,
    update_appointment,
    delete_appointment,
    mark_completed,
)
from app.services.customer import list_customers

router = APIRouter(prefix="/appointments", tags=["appointments"])
templates = Jinja2Templates(directory="templates")


def _parse_date(s: str) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def _parse_time(s: str) -> time | None:
    if not s:
        return None
    try:
        parts = s.split(":")
        if len(parts) >= 2:
            return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        pass
    return None


@router.get("", response_class=HTMLResponse)
def appointments_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointments = list_appointments(db)
    return templates.TemplateResponse(
        "appointments.html",
        {"request": request, "user": current_user, "appointments": appointments},
    )


@router.get("/new", response_class=HTMLResponse)
def appointment_new_form(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customers = list_customers(db)
    return templates.TemplateResponse(
        "appointment_form.html",
        {"request": request, "user": current_user, "customers": customers, "appointment": None},
    )


@router.post("/new", response_class=RedirectResponse)
async def appointment_create(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    form = await request.form()
    try:
        customer_id = int(form.get("customer_id") or 0)
    except ValueError:
        customer_id = 0
    d = _parse_date(form.get("date") or "")
    t = _parse_time(form.get("time") or "")
    notes = (form.get("notes") or "").strip()
    if not customer_id or not d or not t:
        return RedirectResponse(url="/appointments/new?error=missing", status_code=302)
    status = (form.get("status") or "Scheduled").strip()
    if status not in ("Scheduled", "Completed"):
        status = "Scheduled"
    create_appointment(db, customer_id=customer_id, date=d, time=t, notes=notes, status=status)
    return RedirectResponse(url="/appointments", status_code=302)


@router.get("/{appointment_id}/edit", response_class=HTMLResponse)
def appointment_edit_form(
    request: Request,
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = get_appointment_by_id(db, appointment_id)
    if not appointment:
        return RedirectResponse(url="/appointments", status_code=302)
    customers = list_customers(db)
    return templates.TemplateResponse(
        "appointment_form.html",
        {"request": request, "user": current_user, "customers": customers, "appointment": appointment},
    )


@router.post("/{appointment_id}/edit", response_class=RedirectResponse)
async def appointment_update(
    request: Request,
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment_by_id(db, appointment_id)
    if not appointment:
        return RedirectResponse(url="/appointments", status_code=302)
    form = await request.form()
    try:
        customer_id = int(form.get("customer_id") or 0)
    except ValueError:
        customer_id = appointment.customer_id
    d = _parse_date(form.get("date") or "")
    t = _parse_time(form.get("time") or "")
    notes = (form.get("notes") or "").strip()
    status = (form.get("status") or "Scheduled").strip()
    if status not in ("Scheduled", "Completed"):
        status = appointment.status
    if not d:
        d = appointment.date
    if not t:
        t = appointment.time
    if customer_id:
        appointment.customer_id = customer_id
    update_appointment(db, appointment, date=d, time=t, notes=notes, status=status)
    return RedirectResponse(url="/appointments", status_code=302)


@router.post("/{appointment_id}/complete", response_class=RedirectResponse)
def appointment_complete(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment:
        mark_completed(db, appointment)
    return RedirectResponse(url="/appointments", status_code=302)


@router.post("/{appointment_id}/delete", response_class=RedirectResponse)
def appointment_delete(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment:
        delete_appointment(db, appointment)
    return RedirectResponse(url="/appointments", status_code=302)
