# Database Migrations

This directory is designated for schema migration tracking.

## Overview

- In **Phase 1**, baseline schemas are managed directly via modular SQL scripts located in `../schema/`.
- In **Phase 2+**, when the FastAPI backend is integrated, database migrations will be managed using **Alembic** (with `asyncpg` / `SQLAlchemy 2.0` support) or standalone SQL version scripts.

## Migration Convention (Future)

When migrations are generated:
- File naming pattern: `<version>_<description>.sql` (e.g. `0001_initial_schema.sql`, `0002_add_telemedicine_table.sql`)
- Each migration script should be idempotent and include both upgrade and downgrade paths.
