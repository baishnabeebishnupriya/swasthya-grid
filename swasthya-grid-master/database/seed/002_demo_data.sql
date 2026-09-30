-- ==============================================================================
-- SwasthyaGrid Database Seed Data
-- File: 002_demo_data.sql
-- Description: Realistic synthetic demo dataset including beds, staff,
--              attendance, 180-day aggregated epidemiological visit history,
--              180-day medicine consumption history, inventory levels,
--              pre-configured AI demo scenarios, alerts, and redistribution logs.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Beds Allocation per PHC
-- ------------------------------------------------------------------------------
INSERT INTO beds (id, phc_id, total_beds, occupied_beds, reserved_beds, available_beds)
SELECT 
    gen_random_uuid(),
    p.id,
    p.total_beds,
    CASE 
        WHEN p.code = 'OD-PHC-001' THEN 11  -- Balipatna: High occupancy (11/12)
        WHEN p.code = 'WB-PHC-001' THEN 18  -- Diamond Harbour: High occupancy (18/20)
        WHEN p.code = 'JH-PHC-003' THEN 14  -- Ghatshila: High occupancy (14/16)
        ELSE FLOOR(p.total_beds * 0.50)::int
    END AS occupied_beds,
    CASE 
        WHEN p.code = 'OD-PHC-001' THEN 1
        ELSE 1
    END AS reserved_beds,
    p.total_beds - (
        CASE 
            WHEN p.code = 'OD-PHC-001' THEN 11
            WHEN p.code = 'WB-PHC-001' THEN 18
            WHEN p.code = 'JH-PHC-003' THEN 14
            ELSE FLOOR(p.total_beds * 0.50)::int
        END + 1
    ) AS available_beds
FROM phcs p
ON CONFLICT (phc_id) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 2. Synthetic Healthcare Personnel (Staff) - 5-7 per PHC
-- ------------------------------------------------------------------------------
INSERT INTO staff (id, phc_id, employee_code, name, role, specialization, employment_type, is_active, joined_at)
SELECT
    gen_random_uuid(),
    p.id,
    p.code || '-STF-' || LPAD(s.idx::text, 2, '0'),
    s.staff_name,
    s.staff_role,
    s.staff_spec,
    'permanent',
    true,
    CURRENT_DATE - (s.idx * 120 + 300)
FROM phcs p
CROSS JOIN LATERAL (
    VALUES
        (1, 'Dr. Rajesh Mohanty', 'doctor', 'General Medicine / Public Health'),
        (2, 'Dr. Sunita Sen', 'doctor', 'Pediatrics'),
        (3, 'Nurse Anita Das', 'nurse', 'Critical Care & Triage'),
        (4, 'Nurse Priya Kumari', 'nurse', 'General Ward & Immunization'),
        (5, 'Alok Ranjan Mahato', 'pharmacist', 'Pharmacy & Inventory Management'),
        (6, 'Bikash Chandra Roy', 'lab_technician', 'Pathology & Diagnostic Testing'),
        (7, 'Manoj Kumar Panda', 'administrative', 'Health Centre Administration')
) AS s(idx, staff_name, staff_role, staff_spec)
ON CONFLICT (employee_code) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 3. Staff Attendance (Past 14 Days)
-- ------------------------------------------------------------------------------
INSERT INTO attendance (id, staff_id, attendance_date, status, check_in, check_out)
SELECT
    gen_random_uuid(),
    st.id,
    d.att_date::date,
    CASE 
        WHEN EXTRACT(DOW FROM d.att_date) = 0 THEN 'leave' -- Sundays
        WHEN (ABS(HASHTEXT(st.id::text || d.att_date::text)) % 20) = 0 THEN 'absent'
        ELSE 'present'
    END AS status,
    CASE 
        WHEN EXTRACT(DOW FROM d.att_date) = 0 THEN NULL
        ELSE '08:30:00'::time + ((ABS(HASHTEXT(st.id::text || d.att_date::text)) % 30) || ' minutes')::interval
    END AS check_in,
    CASE 
        WHEN EXTRACT(DOW FROM d.att_date) = 0 THEN NULL
        ELSE '17:00:00'::time + ((ABS(HASHTEXT(st.id::text || d.att_date::text)) % 60) || ' minutes')::interval
    END AS check_out
FROM staff st
CROSS JOIN generate_series(CURRENT_DATE - INTERVAL '13 days', CURRENT_DATE, INTERVAL '1 day') AS d(att_date)
ON CONFLICT (staff_id, attendance_date) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 4. 180 Days of Aggregated Patient Visits per PHC (No PII)
--    Models monsoon surges (dengue, malaria, diarrhea, dehydration) and seasonal patterns
-- ------------------------------------------------------------------------------
INSERT INTO patient_visits (id, phc_id, visit_date, disease_category, patient_count, emergency_count)
SELECT
    gen_random_uuid(),
    p.id,
    d.v_date::date,
    c.category,
    GREATEST(0, (
        -- Baseline patient count based on category
        c.base_count
        -- Day of week modulation (Mondays peak)
        + CASE WHEN EXTRACT(DOW FROM d.v_date) = 1 THEN 5 ELSE 0 END
        -- Specific Outbreak surge for PHC A (Balipatna) in past 20 days: Massive diarrhea & dehydration surge
        + CASE 
            WHEN p.code = 'OD-PHC-001' AND c.category IN ('diarrhea', 'dehydration') AND d.v_date >= CURRENT_DATE - INTERVAL '20 days'
            THEN 18 + (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 15)
            ELSE 0
          END
        -- Seasonal monsoon surge (June - Sept approx, or based on day offset)
        + CASE 
            WHEN c.category IN ('dengue', 'malaria') AND (EXTRACT(MONTH FROM d.v_date) IN (6, 7, 8, 9))
            THEN 8 + (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 10)
            ELSE 0
          END
        -- Winter respiratory surge
        + CASE 
            WHEN c.category = 'respiratory' AND (EXTRACT(MONTH FROM d.v_date) IN (11, 12, 1))
            THEN 6 + (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 8)
            ELSE 0
          END
        -- Pseudo-random realistic variation
        + (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 5)
    )) AS patient_count,
    GREATEST(0, (
        CASE 
            WHEN c.category IN ('dehydration', 'malaria', 'injury') 
            THEN (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 4)
            ELSE (ABS(HASHTEXT(p.code || d.v_date::text || c.category)) % 2)
        END
    )) AS emergency_count
FROM phcs p
CROSS JOIN generate_series(CURRENT_DATE - INTERVAL '179 days', CURRENT_DATE, INTERVAL '1 day') AS d(v_date)
CROSS JOIN (
    VALUES
        ('general', 18),
        ('fever', 14),
        ('dengue', 4),
        ('malaria', 5),
        ('respiratory', 9),
        ('diarrhea', 7),
        ('dehydration', 6),
        ('injury', 3),
        ('other', 5)
) AS c(category, base_count)
ON CONFLICT (phc_id, visit_date, disease_category) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 5. 180 Days of Medicine Consumption History (Correlated with Patient Visits)
-- ------------------------------------------------------------------------------
INSERT INTO medicine_consumption (id, phc_id, medicine_id, consumption_date, quantity_consumed)
SELECT
    gen_random_uuid(),
    p.id,
    m.id,
    d.c_date::date,
    GREATEST(1, (
        -- Base consumption
        CASE 
            WHEN m.name LIKE 'Paracetamol%' THEN 35
            WHEN m.name LIKE 'Oral Rehydration Salts%' THEN 20
            WHEN m.name LIKE 'Amoxicillin%' THEN 15
            WHEN m.name LIKE 'Azithromycin%' THEN 10
            WHEN m.name LIKE 'Insulin%' THEN 3
            WHEN m.name LIKE 'IV Normal Saline%' THEN 8
            WHEN m.name LIKE 'Artemisinin%' THEN 6
            WHEN m.name LIKE 'Antimalarial%' THEN 8
            WHEN m.name LIKE 'Doxycycline%' THEN 10
            WHEN m.name LIKE 'Salbutamol%' THEN 4
            WHEN m.name LIKE 'Cetirizine%' THEN 22
            WHEN m.name LIKE 'Metformin%' THEN 25
            WHEN m.name LIKE 'Amlodipine%' THEN 20
            WHEN m.name LIKE 'Zinc Sulfate%' THEN 18
            ELSE 6
        END
        -- Demo Scenario: PHC A (Balipatna) ORS Consumption spikes dramatically over last 20 days
        + CASE 
            WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' AND d.c_date >= CURRENT_DATE - INTERVAL '20 days'
            THEN 35 + (ABS(HASHTEXT(p.code || d.c_date::text || m.name)) % 25)
            ELSE 0
          END
        -- Monsoon antimalarial spike
        + CASE 
            WHEN m.category = 'Antimalarials' AND (EXTRACT(MONTH FROM d.c_date) IN (6, 7, 8, 9))
            THEN 12 + (ABS(HASHTEXT(p.code || d.c_date::text || m.name)) % 10)
            ELSE 0
          END
        + (ABS(HASHTEXT(p.code || d.c_date::text || m.name)) % 6)
    )) AS quantity_consumed
FROM phcs p
CROSS JOIN medicines m
CROSS JOIN generate_series(CURRENT_DATE - INTERVAL '179 days', CURRENT_DATE, INTERVAL '1 day') AS d(c_date)
ON CONFLICT (phc_id, medicine_id, consumption_date) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 6. Current Inventory Levels
--    Includes Demo Scenario:
--    - PHC A (Balipatna, OD-PHC-001): ORS quantity = 15 sachets (CRITICAL SHORTAGE)
--    - PHC B (Pipili, OD-PHC-004): ORS quantity = 1,450 sachets (SURPLUS)
-- ------------------------------------------------------------------------------
INSERT INTO inventory (
    id, phc_id, medicine_id, quantity, reserved_quantity,
    daily_average_consumption, expiry_date, batch_number, last_restocked_at
)
SELECT
    gen_random_uuid(),
    p.id,
    m.id,
    -- Quantity logic
    CASE 
        -- PHC A (Balipatna) ORS: Critical Shortage
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 15
        -- PHC B (Pipili) ORS: Surplus Inventory
        WHEN p.code = 'OD-PHC-004' AND m.name LIKE 'Oral Rehydration Salts%' THEN 1450
        -- Diamond Harbour ACT Antimalarial: Low stock
        WHEN p.code = 'WB-PHC-001' AND m.name LIKE 'Artemisinin%' THEN 45
        -- Standard healthy inventory for others
        ELSE m.reorder_level + (ABS(HASHTEXT(p.code || m.name)) % 400) + 150
    END AS quantity,
    -- Reserved quantity
    CASE 
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 5
        ELSE 10
    END AS reserved_quantity,
    -- Daily average consumption
    CASE 
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 54.50
        WHEN p.code = 'OD-PHC-004' AND m.name LIKE 'Oral Rehydration Salts%' THEN 18.20
        ELSE 22.00
    END AS daily_average_consumption,
    -- Expiry date (12-24 months in future)
    CURRENT_DATE + ((365 + (ABS(HASHTEXT(p.code || m.name)) % 365)) || ' days')::interval AS expiry_date,
    -- Batch Number
    'BAT-' || UPPER(SUBSTRING(p.code FROM 1 FOR 6)) || '-' || LPAD((ABS(HASHTEXT(m.id::text)) % 900 + 100)::text, 4, '0') AS batch_number,
    -- Last restocked
    CURRENT_TIMESTAMP - ((ABS(HASHTEXT(p.code || m.name)) % 30 + 5) || ' days')::interval AS last_restocked_at
FROM phcs p
CROSS JOIN medicines m
ON CONFLICT (phc_id, medicine_id, batch_number) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 7. Future AI Demand Forecasts (Pre-seeded Sample Forecasts for Next 7 Days)
-- ------------------------------------------------------------------------------
INSERT INTO forecasts (id, phc_id, medicine_id, forecast_date, predicted_demand, lower_bound, upper_bound, confidence_score, model_version)
SELECT
    gen_random_uuid(),
    p.id,
    m.id,
    f.f_date::date,
    -- Predicted demand
    CASE 
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 58.00 + (ABS(HASHTEXT(f.f_date::text)) % 8)
        ELSE 22.00 + (ABS(HASHTEXT(f.f_date::text)) % 5)
    END AS predicted_demand,
    CASE 
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 50.00
        ELSE 18.00
    END AS lower_bound,
    CASE 
        WHEN p.code = 'OD-PHC-001' AND m.name LIKE 'Oral Rehydration Salts%' THEN 68.00
        ELSE 28.00
    END AS upper_bound,
    0.9250 AS confidence_score,
    'v1.0.0-xgb-timeseries' AS model_version
FROM phcs p
CROSS JOIN medicines m
CROSS JOIN generate_series(CURRENT_DATE + INTERVAL '1 day', CURRENT_DATE + INTERVAL '7 days', INTERVAL '1 day') AS f(f_date)
WHERE (p.code IN ('OD-PHC-001', 'OD-PHC-004') AND m.name LIKE 'Oral Rehydration Salts%')
   OR (p.code = 'WB-PHC-001' AND m.name LIKE 'Artemisinin%')
ON CONFLICT (phc_id, medicine_id, forecast_date, model_version) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 8. Risk Alerts
-- ------------------------------------------------------------------------------
INSERT INTO risk_alerts (id, phc_id, medicine_id, alert_type, severity, title, description, risk_score, recommended_action, status, created_at)
VALUES
(
    gen_random_uuid(),
    '40000000-0000-0000-0000-000000000001', -- PHC Balipatna
    '30000000-0000-0000-0000-000000000002', -- ORS
    'stockout',
    'critical',
    'Imminent ORS Stockout at PHC Balipatna',
    'Current ORS stock (15 units) will deplete within 8 hours due to acute surge in dehydration and gastroenteritis cases (daily consumption: 54.5 units).',
    94.50,
    'Request immediate inter-PHC resource transfer of 500 ORS sachets from nearby surplus node PHC Pipili (14.2 km).',
    'open',
    CURRENT_TIMESTAMP - INTERVAL '2 hours'
),
(
    gen_random_uuid(),
    '40000000-0000-0000-0000-000000000009', -- PHC Diamond Harbour
    '30000000-0000-0000-0000-000000000007', -- Artemisinin ACT
    'stockout',
    'high',
    'Antimalarial ACT Reserve Depletion Warning',
    'Artemisinin stock is at 45 units (below minimum safe threshold of 100 units) amidst rising monsoon vector cases.',
    78.00,
    'Dispatch replenishment from North 24 Parganas district central warehouse.',
    'open',
    CURRENT_TIMESTAMP - INTERVAL '5 hours'
),
(
    gen_random_uuid(),
    '40000000-0000-0000-0000-000000000018', -- PHC Ghatshila
    NULL,
    'bed_shortage',
    'medium',
    'Bed Capacity Exceeding 85% at PHC Ghatshila',
    'Occupied beds have reached 14/16 beds with 1 bed reserved for triage emergencies.',
    65.00,
    'Coordinate non-critical patient discharges and alert nearby PHC Potka.',
    'acknowledged',
    CURRENT_TIMESTAMP - INTERVAL '1 day'
)
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------------------------
-- 9. Regional Emergency Events
-- ------------------------------------------------------------------------------
INSERT INTO emergency_events (id, name, description, emergency_type, severity, affected_district_id, started_at, status)
VALUES
(
    gen_random_uuid(),
    'Coastal Monsoon Water-Logging & Gastro Surge',
    'Heavy regional rainfall and localized water-logging leading to heightened gastroenteritis, acute diarrhea, and dehydration cases.',
    'flood',
    'high',
    '20000000-0000-0000-0000-000000000001', -- Khordha District
    CURRENT_TIMESTAMP - INTERVAL '3 days',
    'active'
),
(
    gen_random_uuid(),
    'Sundarbans Monsoon Inundation Alert',
    'Tidal river surges affecting coastal lowlands across South 24 Parganas; potential disruption to normal medical supply routes.',
    'cyclone',
    'critical',
    '20000000-0000-0000-0000-000000000004', -- South 24 Parganas
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    'active'
)
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------------------------
-- 10. Resource Transfers (Redistribution Recommendation Demo)
-- ------------------------------------------------------------------------------
INSERT INTO resource_transfers (
    id, source_phc_id, destination_phc_id, resource_type, medicine_id,
    quantity, requested_at, status, distance_km, estimated_arrival_minutes, reason, approved_by
)
VALUES
(
    gen_random_uuid(),
    '40000000-0000-0000-0000-000000000004', -- Source: PHC Pipili (Surplus Node)
    '40000000-0000-0000-0000-000000000001', -- Destination: PHC Balipatna (Shortage Node)
    'medicine',
    '30000000-0000-0000-0000-000000000002', -- ORS
    500,
    CURRENT_TIMESTAMP - INTERVAL '1 hour',
    'recommended',
    14.20,
    35,
    'AI-calculated optimal route rebalance: Rapid transfer of 500 ORS sachets to resolve critical stockout risk at PHC Balipatna.',
    NULL
)
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------------------------
-- 11. Audit Logs (Initial System Telemetry Logs)
-- ------------------------------------------------------------------------------
INSERT INTO audit_logs (id, actor_type, actor_id, action, entity_type, entity_id, metadata, created_at)
VALUES
(
    gen_random_uuid(),
    'system_ai',
    'ai-engine-resilience-monitor',
    'ALERT_GENERATED',
    'risk_alerts',
    '40000000-0000-0000-0000-000000000001',
    '{"reason": "ORS inventory below 8-hour safety buffer", "risk_score": 94.50, "metric": "stockout_risk"}'::jsonb,
    CURRENT_TIMESTAMP - INTERVAL '2 hours'
),
(
    gen_random_uuid(),
    'system_ai',
    'ai-engine-redistribution-optimizer',
    'TRANSFER_RECOMMENDED',
    'resource_transfers',
    '40000000-0000-0000-0000-000000000004',
    '{"source_phc": "PHC Pipili", "dest_phc": "PHC Balipatna", "medicine": "ORS", "qty": 500, "distance_km": 14.2}'::jsonb,
    CURRENT_TIMESTAMP - INTERVAL '1 hour'
)
ON CONFLICT DO NOTHING;
