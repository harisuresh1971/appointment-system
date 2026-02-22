import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()
SECRET_KEY = (os.getenv("SECRET_KEY") or "").strip()

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. On Render: Dashboard -> your service -> Environment -> "
        "Add DATABASE_URL (your Neon or other PostgreSQL connection string)."
    )
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not set. On Render: Dashboard -> your service -> Environment -> "
        "Add SECRET_KEY (any long random string)."
    )
if not (DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")):
    raise ValueError(
        "DATABASE_URL must be a PostgreSQL URL starting with postgresql:// or postgres://. "
        "Check the value in Render Environment."
    )
