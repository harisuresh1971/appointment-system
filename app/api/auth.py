from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user_id
from app.services.auth import get_user_by_email, create_user, authenticate_user, create_token_for_user

router = APIRouter(prefix="", tags=["auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    if get_current_user_id(request) is not None:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("register.html", {"request": request, "user": None})


@router.post("/register", response_class=RedirectResponse)
async def register_submit(
    request: Request,
    db: Session = Depends(get_db),
):
    form = await request.form()
    email = (form.get("email") or "").strip()
    password = form.get("password") or ""
    if not email or not password:
        return RedirectResponse(url="/register?error=missing", status_code=302)
    if get_user_by_email(db, email):
        return RedirectResponse(url="/register?error=exists", status_code=302)
    create_user(db, email=email, password=password)
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if get_current_user_id(request) is not None:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@router.post("/login", response_class=RedirectResponse)
async def login_submit(
    request: Request,
    db: Session = Depends(get_db),
):
    form = await request.form()
    email = (form.get("email") or "").strip()
    password = form.get("password") or ""
    if not email or not password:
        return RedirectResponse(url="/login?error=missing", status_code=302)
    user = authenticate_user(db, email=email, password=password)
    if not user:
        return RedirectResponse(url="/login?error=invalid", status_code=302)
    token = create_token_for_user(user)
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return response


@router.get("/logout", response_class=RedirectResponse)
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
