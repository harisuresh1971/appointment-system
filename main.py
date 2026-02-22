from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Load config and DB early; print clear error so Render logs show it
try:
    import app.core.database  # noqa: F401
except Exception as e:
    import sys
    print("STARTUP ERROR (check Render Environment):", str(e), file=sys.stderr)
    raise

from app.api import auth, dashboard, customers, appointments

app = FastAPI(title="Appointment System")

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
