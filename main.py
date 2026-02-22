from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import app.core.database
from app.api import auth, dashboard, customers, appointments

app = FastAPI(title="Appointment System")
templates = Jinja2Templates(directory="templates")

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
