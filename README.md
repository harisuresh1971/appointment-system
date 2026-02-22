# Appointment System

## Local run

1. Create a PostgreSQL database and set `DATABASE_URL` and `SECRET_KEY` in a `.env` file (see `.env.example`).

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the application:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open http://localhost:8000 in a browser. Register a user, then log in. Tables are created on first run.

---

## Deploy on Render (recommended) — get your live link

This app is a **FastAPI + PostgreSQL** backend with server-rendered pages. **Render** is the right place to deploy it. (Vercel and Vite are for frontend/static or serverless; this app needs a long-running server and a database.)

### Option A: One-click with Blueprint (creates app + database)

1. Push this project to **GitHub** (create a repo and push your code).
2. Go to [https://dashboard.render.com](https://dashboard.render.com) and sign in (or sign up with GitHub).
3. Click **New** → **Blueprint**.
4. Connect your GitHub account if needed, then select the repo that has this project.
5. Render will read `render.yaml` and create:
   - A **PostgreSQL** database (free tier).
   - A **Web Service** that uses it.
6. Click **Apply** and wait for the first deploy to finish.
7. Your live link will be: **`https://<your-service-name>.onrender.com`**  
   (e.g. `https://appointment-system.onrender.com` if you keep the name from `render.yaml`).

### Option B: Manual Web Service (you already have a database)

1. Push this project to **GitHub**.
2. On Render: **New** → **Web Service**.
3. Connect the repo and select it.
4. Use:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment**, add:
   - `DATABASE_URL` — your PostgreSQL connection string (from Render PostgreSQL or elsewhere).
   - `SECRET_KEY` — a long random string (e.g. from `openssl rand -hex 32`).
6. Click **Create Web Service**. When the deploy succeeds, your link is **`https://<service-name>.onrender.com`**.

### After deploy

- Open the link → you should see a redirect to `/login`.
- Register a user, log in, and use Dashboard, Customers, and Appointments.
- Free-tier services spin down after inactivity; the first open may take 30–60 seconds.
