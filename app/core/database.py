from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL

# Neon and some hosts use postgres://; SQLAlchemy 2 prefers postgresql://
_db_url = DATABASE_URL
if _db_url.startswith("postgres://"):
    _db_url = "postgresql://" + _db_url[11:]

try:
    engine = create_engine(_db_url)
except Exception as e:
    raise RuntimeError(
        "Could not connect to database. Check DATABASE_URL in Render Environment "
        "(e.g. from Neon.tech). It must be a valid PostgreSQL URL."
    ) from e
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.models import user, customer, appointment
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
