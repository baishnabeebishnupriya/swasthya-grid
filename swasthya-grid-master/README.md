# SwasthyaGrid 🇮🇳 
### AI-Powered Health Resource Resilience Network for India's Primary Health Centres (PHCs)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15.x-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4+-green?logo=postgis&logoColor=white)](https://postgis.net)
[![Scikit--Learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Tests](https://img.shields.io/badge/Pytest-25%20Passed-brightgreen)](https://pytest.org)

SwasthyaGrid is an enterprise health resource intelligence and logistics platform designed for India's 30,000+ Primary Health Centres (PHCs). It couples real-time telemetry across medicine inventory, bed capacity, staffing, and clinical demand with predictive AI and geospatial optimization to anticipate stockouts, score facility resilience, and recommend peer-to-peer resource redistribution.

---

## 🏛️ System Architecture

```text
Next.js 15 Command Center (App Router)
                 │ (REST / Bearer JWT)
                 ▼
       FastAPI Backend Gateway
   ┌─────────────┼─────────────┐
   ▼             ▼             ▼
AI Engine   RBAC & Audit   Database Layer
(Joblib)    (Bcrypt/JWT)   (SQLAlchemy / Asyncpg)
                               │
                               ▼
                    PostgreSQL 16 + PostGIS
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 15 (App Router, React 19), Tailwind CSS, Lucide React, Leaflet, Recharts |
| **Backend** | FastAPI, Uvicorn, Pydantic v2, Pydantic-Settings |
| **Database & GIS** | PostgreSQL 16, PostGIS 3.4, SQLAlchemy 2.x (asyncio), `asyncpg`, GeoAlchemy2, Alembic |
| **AI & Forecasting** | Scikit-Learn (RandomForest Multi-horizon Forecaster), NumPy, Pandas, Joblib |
| **Security & Auth** | Bcrypt (12 rounds salted hash), PyJWT (HS256 claims), Scope Verification |
| **Testing & CI** | Pytest, Pytest-Asyncio, HTTPX |

---

## 🚀 Quick Start (Local Development)

### 1. Database Setup
Ensure a local PostgreSQL instance with PostGIS is running, or start via Docker:
```bash
docker run --name swasthyagrid_db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=swasthyagrid -p 5432:5432 -d postgis/postgis:16-3.4
```

Apply database migrations and seed data:
```bash
cd backend
alembic upgrade head
```

### 2. Start Backend API
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate | On Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
API Documentation will be available at `http://127.0.0.1:8000/docs`.

### 3. Start Frontend Command Center
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🐳 Docker Compose Deployment

To launch the complete unified stack with a single command:
```bash
docker-compose up --build
```
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

---

## 🛡️ Role-Based Access Control & Demo Accounts

SwasthyaGrid enforces three distinct operational tiers:

| Role | Synthetic Demo Officer | Email Address | Password | Scope |
|---|---|---|---|---|
| **`STATE_ADMIN`** | Dr. Rajeshwar Jena | `state.admin@odisha.health.gov.in` | `Password@123` | Odisha State |
| **`DISTRICT_OFFICER`** | Dr. Manas Ranjan Samal | `district.khordha@odisha.health.gov.in` | `Password@123` | Khordha District |
| **`PHC_ADMIN`** | Dr. Priya Darshini Mohanty | `phc.balipatna@odisha.health.gov.in` | `Password@123` | PHC Balipatna (`OD-PHC-001`) |
| **`PHC_ADMIN`** | Dr. Alok Nath Tripathy | `phc.pipili@odisha.health.gov.in` | `Password@123` | PHC Pipili (`OD-PHC-004`) |

---

## 🧪 Testing & Verification

Run the comprehensive 25-test backend test suite:
```bash
cd backend
pytest
```

Run frontend production build verification:
```bash
cd frontend
npm run build
```

---

## ☁️ Production Cloud Deployment

For step-by-step instructions on deploying SwasthyaGrid to **Supabase** (Database), **Render / Railway** (FastAPI Backend), and **Vercel** (Next.js Frontend), refer to the detailed [Deployment Guide](docs/DEPLOYMENT_GUIDE.md).

---

## 🔒 Security Summary

- **Bcrypt Password Encryption**: Salted hashes generated with 12 rounds; plaintext passwords are never stored.
- **Stateless JWT Authorization**: Minimum necessary claims (`user_id`, `role`, `state_id`, `district_id`, `phc_id`) signed with `HS256`.
- **Scope & Tenant Isolation**: Medical Officers are isolated to designated facilities; District Officers to assigned administrative clusters.
- **Audit Logging**: Sensitive governance events (Logins, Bed updates, Transfer Authorizations) are recorded to `audit_logs`.
- **Zero Secrets in Source**: All API keys, database credentials, and cryptographic secrets are sourced from environment variables.

---

## 📋 MVP Scope & Known Limitations

1. **Token Revocation**: Current authentication uses stateless JWT with audit log tracking; production scaling can integrate Redis for distributed blacklisting.
2. **Federated Model Learning**: Scheduled for post-MVP phase; current AI models utilize centralized chronological training with time-series feature engineering.
