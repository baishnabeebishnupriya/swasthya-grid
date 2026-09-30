-- ==============================================================================
-- SwasthyaGrid Synthetic Seed Data
-- File: 003_seed_users.sql
-- Description: Seed users for Role-Based Access Control (RBAC) testing.
-- Note: All synthetic demo accounts use standard development credentials:
--       Password: Password@123 (hashed with bcrypt)
-- ==============================================================================

INSERT INTO users (id, name, email, password_hash, role, state_id, district_id, phc_id, is_active)
VALUES
    -- 1. STATE_ADMIN: Odisha State Health Director
    (
        '50000000-0000-0000-0000-000000000001',
        'Dr. Rajeshwar Jena',
        'state.admin@odisha.health.gov.in',
        '$2b$12$D6i03y9MXQ.Qlo52TUODjO1nXYxP5upfjzEtAVurbElfZDd4AOIrK',
        'STATE_ADMIN',
        '10000000-0000-0000-0000-000000000001',  -- Odisha
        NULL,
        NULL,
        true
    ),
    -- 2. DISTRICT_OFFICER: Chief District Medical Officer (Khordha District)
    (
        '50000000-0000-0000-0000-000000000002',
        'Dr. Manas Ranjan Samal',
        'district.khordha@odisha.health.gov.in',
        '$2b$12$D6i03y9MXQ.Qlo52TUODjO1nXYxP5upfjzEtAVurbElfZDd4AOIrK',
        'DISTRICT_OFFICER',
        '10000000-0000-0000-0000-000000000001',  -- Odisha
        '20000000-0000-0000-0000-000000000001',  -- Khordha
        NULL,
        true
    ),
    -- 3. PHC_ADMIN: Medical Officer In-Charge (PHC Balipatna)
    (
        '50000000-0000-0000-0000-000000000003',
        'Dr. Priya Darshini Mohanty',
        'phc.balipatna@odisha.health.gov.in',
        '$2b$12$D6i03y9MXQ.Qlo52TUODjO1nXYxP5upfjzEtAVurbElfZDd4AOIrK',
        'PHC_ADMIN',
        '10000000-0000-0000-0000-000000000001',  -- Odisha
        '20000000-0000-0000-0000-000000000001',  -- Khordha
        '40000000-0000-0000-0000-000000000001',  -- PHC Balipatna
        true
    ),
    -- 4. PHC_ADMIN: Medical Officer In-Charge (PHC Pipili)
    (
        '50000000-0000-0000-0000-000000000004',
        'Dr. Alok Nath Tripathy',
        'phc.pipili@odisha.health.gov.in',
        '$2b$12$D6i03y9MXQ.Qlo52TUODjO1nXYxP5upfjzEtAVurbElfZDd4AOIrK',
        'PHC_ADMIN',
        '10000000-0000-0000-0000-000000000001',  -- Odisha
        '20000000-0000-0000-0000-000000000002',  -- Puri
        '40000000-0000-0000-0000-000000000004',  -- PHC Pipili
        true
    )
ON CONFLICT (email) DO UPDATE 
SET password_hash = EXCLUDED.password_hash,
    name = EXCLUDED.name,
    role = EXCLUDED.role,
    updated_at = CURRENT_TIMESTAMP;
