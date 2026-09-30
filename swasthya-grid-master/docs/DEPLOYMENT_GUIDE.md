# SwasthyaGrid Production Cloud Deployment Guide

A step-by-step guide to deploying the SwasthyaGrid platform across managed cloud infrastructure.

---

## 🏗️ Target Production Architecture

$$\text{User Browser} \longrightarrow \underbrace{\text{Vercel (Next.js 15 Frontend)}}_{\text{NEXT\_PUBLIC\_API\_URL}} \longrightarrow \underbrace{\text{Render / Railway (FastAPI Backend)}}_{\text{DATABASE\_URL, JWT\_SECRET\_KEY, CORS\_ORIGINS}} \longrightarrow \underbrace{\text{Supabase / Neon (PostgreSQL + PostGIS)}}_{\text{16 Tables, GiST Indexes}}$$

---

## Step 1: Managed Database Setup (e.g. Supabase / Neon / Render Postgres)

1. **Create a Managed PostgreSQL Instance**:
   - Provision a PostgreSQL 15+ or 16+ instance.
   - Note the **Connection String** (URI format).

2. **Enable Required Extensions**:
   Execute the following in the database SQL editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

3. **Initialize Schema & Seed Data**:
   - Option A: Run Alembic migrations from backend:
     ```bash
     export DATABASE_URL="postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>?ssl=require"
     alembic upgrade head
     ```
   - Option B: Execute the migration scripts directly in SQL editor:
     1. `database/schema/002_tables.sql`
     2. `database/schema/003_indexes.sql`
     3. `database/seed/001_reference_data.sql`
     4. `database/seed/002_synthetic_operational_data.sql`
     5. `database/seed/003_seed_users.sql`

---

## Step 2: Backend API Deployment (e.g. Render / Railway)

1. **Create a New Web Service**:
   - Connect your Git repository.
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3` or `Docker`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2`

2. **Configure Environment Variables**:
   In the Render/Railway Dashboard, add:
   - `APP_NAME`: `SwasthyaGrid API`
   - `APP_ENV`: `production`
   - `DATABASE_URL`: `postgresql+asyncpg://<username>:<password>@<db-host>:<port>/<dbname>?ssl=require`
   - `JWT_SECRET_KEY`: *(Generate a secure 64-character random string)*
   - `JWT_ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `720`
   - `REFRESH_TOKEN_EXPIRE_DAYS`: `7`
   - `CORS_ORIGINS`: `https://your-frontend-domain.vercel.app` *(update once frontend is deployed)*

3. **Verify Deployment**:
   Test health checks in your browser:
   - `https://your-backend-api.onrender.com/api/health`
   - `https://your-backend-api.onrender.com/api/health/database`

---

## Step 3: Frontend Command Center Deployment (Vercel)

1. **Import Project into Vercel**:
   - Connect your GitHub repository.
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`

2. **Configure Environment Variables**:
   In the Vercel Project Settings:
   - `NEXT_PUBLIC_API_URL`: `https://your-backend-api.onrender.com` *(pointing to your deployed backend)*

3. **Deploy**:
   - Click **Deploy**. Vercel will automatically run `npm run build` and provision edge CDN distribution.

4. **Complete CORS Pairing**:
   - Copy your assigned Vercel URL (e.g., `https://swasthya-grid.vercel.app`).
   - Add this domain to `CORS_ORIGINS` in your backend environment variables and redeploy the backend.

---

## Step 4: Verification & Smoke Test

1. Visit your Vercel URL (`https://swasthya-grid.vercel.app`).
2. Log in using one of the synthetic administrative demo accounts:
   - **State Admin**: `state.admin@odisha.health.gov.in` / `Password@123`
   - **District Officer**: `district.khordha@odisha.health.gov.in` / `Password@123`
   - **PHC Admin**: `phc.balipatna@odisha.health.gov.in` / `Password@123`
3. Verify that telemetry cards, Leaflet map markers, AI forecast charts, and redistribution transfer authorizations operate interactively.
