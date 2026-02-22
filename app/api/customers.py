from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import TEMPLATES_DIR
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.customer import (
    list_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    get_customer_by_phone,
)

router = APIRouter(prefix="/customers", tags=["customers"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("", response_class=HTMLResponse)
def customers_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customers = list_customers(db)
    return templates.TemplateResponse(
        "customers.html",
        {"request": request, "user": current_user, "customers": customers},
    )


@router.get("/new", response_class=HTMLResponse)
def customer_new_form(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "customer_form.html",
        {"request": request, "user": current_user, "customer": None},
    )


@router.post("/new", response_class=RedirectResponse)
async def customer_create(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    form = await request.form()
    name = (form.get("name") or "").strip()
    phone = (form.get("phone") or "").strip()
    if not name or not phone:
        return RedirectResponse(url="/customers/new?error=missing", status_code=302)
    if get_customer_by_phone(db, phone):
        return RedirectResponse(url="/customers/new?error=duplicate_phone", status_code=302)
    create_customer(db, name=name, phone=phone)
    return RedirectResponse(url="/customers", status_code=302)


@router.get("/{customer_id}/edit", response_class=HTMLResponse)
def customer_edit_form(
    request: Request,
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return RedirectResponse(url="/customers", status_code=302)
    return templates.TemplateResponse(
        "customer_form.html",
        {"request": request, "user": current_user, "customer": customer},
    )


@router.post("/{customer_id}/edit", response_class=RedirectResponse)
async def customer_update(
    request: Request,
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return RedirectResponse(url="/customers", status_code=302)
    form = await request.form()
    name = (form.get("name") or "").strip()
    phone = (form.get("phone") or "").strip()
    if not name or not phone:
        return RedirectResponse(url=f"/customers/{customer_id}/edit?error=missing", status_code=302)
    existing = get_customer_by_phone(db, phone)
    if existing and existing.id != customer_id:
        return RedirectResponse(url=f"/customers/{customer_id}/edit?error=duplicate_phone", status_code=302)
    update_customer(db, customer, name=name, phone=phone)
    return RedirectResponse(url="/customers", status_code=302)


@router.post("/{customer_id}/delete", response_class=RedirectResponse)
def customer_delete(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = get_customer_by_id(db, customer_id)
    if customer:
        delete_customer(db, customer)
    return RedirectResponse(url="/customers", status_code=302)
