import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse

# Load config and DB early; print clear error so Render logs show it
try:
    import app.core.database  # noqa: F401
except Exception as e:
    print("STARTUP ERROR (check Render Environment):", str(e), file=sys.stderr)
    raise

from app.api import auth, dashboard, customers, appointments

app = FastAPI(title="Appointment System")


@app.exception_handler(Exception)
def catch_all_exception_handler(request: Request, exc: Exception):
    """Log the real error so it appears in Render logs, then return a friendly 500 page."""
    tb = traceback.format_exc()
    print("INTERNAL SERVER ERROR:", tb, file=sys.stderr)
    return HTMLResponse(
        content="<h1>Something went wrong</h1><p>Check the server logs for details.</p>",
        status_code=500,
    )


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(customers.router)
app.include_router(appointments.router)


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard", status_code=302)


@app.get("/health")
def health():
    return {"status": "ok"}
