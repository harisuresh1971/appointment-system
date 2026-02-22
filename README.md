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

## Deploy FREE on Render (no credit card)

Use a **free Render Web Service** plus a **free PostgreSQL** from Neon. Everything stays free.

### Step 1: Get a free PostgreSQL database

1. Go to **[Neon.tech](https://neon.tech)** and sign up (free, no card).
2. Create a new project. Copy the **connection string** (looks like `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`). This is your `DATABASE_URL`.

### Step 2: Deploy the app on Render

1. Go to **[dashboard.render.com](https://dashboard.render.com)** and sign in with GitHub.
2. Click **New** → **Web Service**.
3. Connect the repo **harisuresh1971/appointment-system** (or your fork).
4. Use:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Select **Free** plan (not paid).
6. **Important — add Environment variables before first deploy:**
   - Click **Environment** (or **Advanced** → **Add Environment Variable**).
   - Add **Key:** `DATABASE_URL` → **Value:** paste the full Neon connection string from Step 1 (e.g. `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`).
   - Add **Key:** `SECRET_KEY` → **Value:** any long random string (e.g. `my-secret-key-12345-change-in-production`).
   - Save. Without these two, the deploy will fail.
7. Click **Create Web Service**. Wait for the deploy to finish.

Your app will be at **https://appointment-system.onrender.com** (or the name you chose). Open it, register, and log in.

### Free tier notes

- Render free services **spin down** after ~15 minutes of no traffic; first open may take 30–60 seconds.
- Neon free tier is enough for this app; no card required.

### Alternative free Postgres

You can use **[ElephantSQL](https://www.elephantsql.com)** or **[Supabase](https://supabase.com)** free tier instead of Neon. Create a database, copy the PostgreSQL URL, and use it as `DATABASE_URL` in Render.
