from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User


def get_current_user_id(request: Request) -> int | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        return None
    try:
        return int(payload["sub"])
    except (ValueError, TypeError):
        return None


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User | RedirectResponse:
    user_id = get_current_user_id(request)
    if user_id is None:
        return RedirectResponse(url="/login", status_code=302)
    user = db.get(User, user_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return user
