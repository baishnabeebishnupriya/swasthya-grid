# SwasthyaGrid Backend REST API & AI Decision Service

The FastAPI backend powering the **SwasthyaGrid** Health Resource Resilience Network.

---

## 🏛️ Architecture & Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **ASGI Server**: Uvicorn
- **Database ORM**: SQLAlchemy 2.x (asyncio) + `asyncpg`
- **Spatial Extension**: PostGIS + GeoAlchemy2
- **Data Validation & Settings**: Pydantic v2 + Pydantic-Settings
- **Security**: Direct `bcrypt` password hashing (12 rounds) + `pyjwt` (HS256)
- **AI & Analytics**: Scikit-Learn (RandomForest Time-Series Forecaster), NumPy, Pandas
- **Migrations**: Alembic

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description | Example / Default |
|---|---|---|
| `APP_NAME` | Service Display Name | `SwasthyaGrid API` |
| `APP_ENV` | Environment (`development`, `production`) | `production` |
| `HOST` | Bind host address | `0.0.0.0` |
| `PORT` | Bind port number (dynamic on Render/Railway) | `8000` |
| `DATABASE_URL` | PostgreSQL + PostGIS connection string | `postgresql+asyncpg://user:pass@host:5432/swasthyagrid` |
| `JWT_SECRET_KEY` | 64-char cryptographically secure secret | Sourced from environment |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifespan in minutes | `720` (12 hours) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifespan in days | `7` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins | `http://localhost:3000,https://swasthyagrid.vercel.app` |

---

## 🚀 Commands

### 1. Local Development
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Production Startup
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
```

### 3. Run Database Migrations
```bash
alembic upgrade head
```

### 4. Retrain AI Demand Forecasting Model
```bash
python -m app.ai.train
```

### 5. Run Test Suite
```bash
pytest
```

---

## 🩺 Health Check Endpoints

- `GET /api/health`: Basic uptime and API heartbeat check.
- `GET /api/health/database`: Verifies PostgreSQL + PostGIS connectivity and returns active connection pool status (safely redacting credentials).
