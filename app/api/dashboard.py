from datetime import date, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.appointment import get_today_appointments, list_appointments

router = APIRouter(prefix="", tags=["dashboard"])
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    today_list = get_today_appointments(db, today)
    upcoming_list = list_appointments(db, from_date=tomorrow)[:20]
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "today_appointments": today_list,
            "upcoming_appointments": upcoming_list,
        },
    )
