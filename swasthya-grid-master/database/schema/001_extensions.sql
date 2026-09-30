-- ==============================================================================
-- SwasthyaGrid Database Schema
-- File: 001_extensions.sql
-- Description: Enables required PostgreSQL extensions for UUIDs, Cryptography,
--              and PostGIS spatial operations.
-- ==============================================================================

-- Enable UUID generation support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enable PostGIS spatial database extension for geographical coordinates and distance calculations
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Enable btree_gist for advanced indexing (combining spatial and standard scalar indexes)
CREATE EXTENSION IF NOT EXISTS "btree_gist";
