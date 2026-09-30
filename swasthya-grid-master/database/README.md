# SwasthyaGrid Database Layer 🗄️

This directory contains the complete database layer for **SwasthyaGrid** (Phase 1): SQL schemas, spatial PostGIS configurations, performance indexes, domain integrity constraints, and reproducible synthetic seed datasets.

---

## 1. Purpose of the Database

SwasthyaGrid operates as a resilience and resource allocation network for India's Primary Health Centres (PHCs). The database layer is engineered to:
- Model administrative and geographic hierarchies (`states` → `districts` → `phcs`).
- Perform geospatial queries and proximity calculations via **PostGIS** (`ST_Distance`, `ST_DWithin`).
- Maintain supply chain visibility (`medicines`, `inventory`, `beds`, `staff`, `attendance`).
- Store high-frequency epidemiological time series (`patient_visits`, `medicine_consumption`).
- Support AI-driven resilience optimization (`forecasts`, `risk_alerts`, `resource_transfers`, `emergency_events`, `audit_logs`).

---

## 2. PostgreSQL + PostGIS Architecture

- **Engine**: PostgreSQL 14+ with PostGIS 3.x
- **Coordinates & Spatial SRID**: `SRID 4326` (WGS 84 standard GPS latitude/longitude) using `geography(Point, 4326)` for geodesic distance computations in meters/kilometers without map projection distortion.
- **Key Extensions**:
  - `uuid-ossp` / `pgcrypto`: Cryptographic UUID primary keys (`gen_random_uuid()`).
  - `postgis`: Geospatial objects, indexing, and geodesic spatial operations.
  - `btree_gist`: Multidimensional and combined GiST indexing.

---

## 3. Entity-Relationship (ER) Diagram

```
 states (1) ───< districts (N) ───< phcs (N)
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │ (1:1)                      │ (1:N)                      │ (1:N)
         ▼                            ▼                            ▼
       beds                         staff                      inventory >─── (N:1) medicines
                                      │                            │
                                      ▼ (1:N)                      ▼ (1:N)
                                  attendance              medicine_consumption
                                                                   │
                                                                   ▼ (N:1)
                                                               medicines
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │ (1:N)                      │ (1:N)                      │ (1:N)
         ▼                            ▼                            ▼
   patient_visits                 forecasts                   risk_alerts
                                      │                            │
                                      ▼ (N:1)                      ▼ (N:1)
                                  medicines                    medicines

 resource_transfers:
   source_phc_id      ───> phcs(id)
   destination_phc_id ───> phcs(id)
   medicine_id        ───> medicines(id) [nullable]

 emergency_events:
   affected_district_id ─> districts(id) [nullable]

 audit_logs:
   actor_type, actor_id, entity_type, entity_id, metadata (JSONB)
```

---

## 4. Directory Structure

```
database/
├── README.md
├── schema/
│   ├── 001_extensions.sql     # PostGIS, UUID, pgcrypto, btree_gist
│   ├── 002_tables.sql         # DDL for all 15 core and AI tables
│   ├── 003_indexes.sql        # Spatial (GiST), compound, and B-Tree indexes
│   └── 004_constraints.sql    # Business domain CHECK, UNIQUE, and FK rules
├── seed/
│   ├── 001_reference_data.sql # 3 States, 8 Districts, 15 Medicines, 20 PHCs
│   └── 002_demo_data.sql      # Beds, Staff, 180-day Visits & Consumption, AI Demo data
└── migrations/
    └── README.md              # Migration policies for future backend integration
```

---

## 5. Database Setup & Loading Instructions

### Prerequisites
- PostgreSQL 14 or higher installed.
- PostGIS extension available on your PostgreSQL server.

### Step 1: Create the Database
Open your terminal (PowerShell, bash, or `psql`) and create a dedicated database:

```bash
# Connect as postgres admin user
psql -U postgres -h localhost -c "CREATE DATABASE swasthyagrid;"
```

### Step 2: Run Schema Files (In Order)
Execute the schema files sequentially against the `swasthyagrid` database:

```bash
# Windows PowerShell / Linux / macOS
psql -U postgres -h localhost -d swasthyagrid -f database/schema/001_extensions.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/002_tables.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/003_indexes.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/004_constraints.sql
```

### Step 3: Run Seed Files (In Order)
Populate static reference data followed by the synthetic demo datasets:

```bash
psql -U postgres -h localhost -d swasthyagrid -f database/seed/001_reference_data.sql
psql -U postgres -h localhost -d swasthyagrid -f database/seed/002_demo_data.sql
```

### One-Line Reset & Recreate (Development Script)
To wipe and completely reload during development:

```bash
psql -U postgres -h localhost -d swasthyagrid -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
psql -U postgres -h localhost -d swasthyagrid -f database/schema/001_extensions.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/002_tables.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/003_indexes.sql
psql -U postgres -h localhost -d swasthyagrid -f database/schema/004_constraints.sql
psql -U postgres -h localhost -d swasthyagrid -f database/seed/001_reference_data.sql
psql -U postgres -h localhost -d swasthyagrid -f database/seed/002_demo_data.sql
```

---

## 6. Demo Scenario Details (Pre-Seeded for Phase 2 AI Verification)

The seed data establishes the following scenario:

- **Deficit Node**: **PHC Balipatna** (`OD-PHC-001`) in Khordha District, Odisha.
  - Recent 20-day cluster of gastroenteritis / dehydration cases (`patient_visits`).
  - Daily ORS consumption surged to ~54.5 sachets/day (`medicine_consumption`).
  - Current ORS stock: **15 sachets** (critically below minimum threshold of 200).
  - Risk status: `critical` (Risk score 94.50 in `risk_alerts`).
- **Surplus Node**: **PHC Pipili** (`OD-PHC-004`) in Puri District, Odisha.
  - Normal consumption: ~18.2 sachets/day.
  - Current ORS stock: **1,450 sachets** (surplus > 900 sachets).
  - Proximity: **14.2 km** geodesic distance from PHC Balipatna.
- **Redistribution Action**:
  - `resource_transfers` pre-contains a recommended transfer of **500 ORS sachets** from PHC Pipili to PHC Balipatna (ETA: 35 minutes).

---

## 7. How the FastAPI Backend Connects (Phase 2 Preview)

The backend will connect via asynchronous SQLAlchemy or asyncpg using standard environment variables:

```env
DATABASE_URL=postgresql+asyncpg://swasthya_user:secret_password@localhost:5432/swasthyagrid
```

- Connection pooling (e.g. `pool_size=20`, `max_overflow=10`).
- Read-only replicas for analytics/forecasting if scaled.
- GeoAlchemy2 for PostGIS ORM mappings.

---

## 8. Security Considerations

1. **Direct Access Ban**: The Next.js frontend MUST NEVER connect directly to PostgreSQL. All requests route through FastAPI.
2. **Principle of Least Privilege**: In production, create a dedicated `swasthya_app` role with `SELECT, INSERT, UPDATE, DELETE` permissions only, restricting `DDL` execution.
3. **No Hardcoded Credentials**: Passwords and connection strings must be injected via environment variables (`.env`).
4. **Audit Logging**: Sensitive changes (transfers, inventory adjustments, emergency events) are tracked in `audit_logs`.

---

## 9. Synthetic Data Disclaimer

> **DISCLAIMER**: All patient visit records, illness counts, medicine consumption numbers, and staff names in this dataset are **100% synthetic and generated for demonstration and research benchmarking purposes**. No personally identifiable health information (PHI/PII) is captured or stored.
