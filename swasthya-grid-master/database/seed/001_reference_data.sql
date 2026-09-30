-- ==============================================================================
-- SwasthyaGrid Database Seed Data
-- File: 001_reference_data.sql
-- Description: Static Master & Reference Data (States, Districts, Medicines, PHCs)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- States (3 States: Odisha, West Bengal, Jharkhand)
-- ------------------------------------------------------------------------------
INSERT INTO states (id, name, code) VALUES
('10000000-0000-0000-0000-000000000001', 'Odisha', 'OD'),
('10000000-0000-0000-0000-000000000002', 'West Bengal', 'WB'),
('10000000-0000-0000-0000-000000000003', 'Jharkhand', 'JH')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, code = EXCLUDED.code;

-- ------------------------------------------------------------------------------
-- Districts (8 Districts across 3 States)
-- ------------------------------------------------------------------------------
INSERT INTO districts (id, state_id, name, code) VALUES
-- Odisha
('20000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'Khordha', 'OD_KHO'),
('20000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000001', 'Puri', 'OD_PUR'),
('20000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000001', 'Cuttack', 'OD_CUT'),
-- West Bengal
('20000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000002', 'South 24 Parganas', 'WB_S24'),
('20000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000002', 'North 24 Parganas', 'WB_N24'),
('20000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000002', 'Howrah', 'WB_HWH'),
-- Jharkhand
('20000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000003', 'Ranchi', 'JH_RAN'),
('20000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000003', 'East Singhbhum', 'JH_ESB'),
('20000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000003', 'Dhanbad', 'JH_DHN')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, code = EXCLUDED.code;

-- ------------------------------------------------------------------------------
-- Medicines (15 Essential Primary Healthcare Drugs & Supplies)
-- ------------------------------------------------------------------------------
INSERT INTO medicines (id, name, generic_name, category, unit, minimum_stock_level, reorder_level) VALUES
('30000000-0000-0000-0000-000000000001', 'Paracetamol 500mg', 'Paracetamol', 'Analgesics & Antipyretics', 'tablets', 500, 1000),
('30000000-0000-0000-0000-000000000002', 'Oral Rehydration Salts (ORS)', 'Oral Rehydration Salts IP', 'Gastrointestinal & Electrolytes', 'sachets', 200, 500),
('30000000-0000-0000-0000-000000000003', 'Amoxicillin 500mg', 'Amoxicillin Trihydrate', 'Antibiotics', 'capsules', 300, 600),
('30000000-0000-0000-0000-000000000004', 'Azithromycin 500mg', 'Azithromycin', 'Antibiotics', 'tablets', 150, 300),
('30000000-0000-0000-0000-000000000005', 'Insulin (Regular) 100IU/ml', 'Human Insulin (rDNA)', 'Antidiabetic', 'vials', 30, 60),
('30000000-0000-0000-0000-000000000006', 'IV Normal Saline 0.9%', 'Sodium Chloride 0.9% w/v', 'Intravenous Fluids', 'bottles', 100, 250),
('30000000-0000-0000-0000-000000000007', 'Artemisinin Combo (ACT)', 'Artemether + Lumefantrine', 'Antimalarials', 'tablets', 100, 200),
('30000000-0000-0000-0000-000000000008', 'Antimalarial (Chloroquine)', 'Chloroquine Phosphate 250mg', 'Antimalarials', 'tablets', 200, 400),
('30000000-0000-0000-0000-000000000009', 'Doxycycline 100mg', 'Doxycycline Hyclate', 'Antibiotics', 'capsules', 150, 300),
('30000000-0000-0000-0000-000000000010', 'Salbutamol Inhaler 100mcg', 'Salbutamol Sulfate', 'Respiratory', 'canisters', 25, 50),
('30000000-0000-0000-0000-000000000011', 'Cetirizine 10mg', 'Cetirizine Hydrochloride', 'Antihistamines', 'tablets', 400, 800),
('30000000-0000-0000-0000-000000000012', 'Metformin 500mg', 'Metformin Hydrochloride', 'Antidiabetic', 'tablets', 400, 800),
('30000000-0000-0000-0000-000000000013', 'Amlodipine 5mg', 'Amlodipine Besylate', 'Cardiovascular', 'tablets', 300, 600),
('30000000-0000-0000-0000-000000000014', 'Zinc Sulfate 20mg', 'Zinc Sulfate Dispersible', 'Pediatric & Nutritional', 'tablets', 300, 600),
('30000000-0000-0000-0000-000000000015', 'IV Dextrose 5%', 'Dextrose Anhydrous 5% w/v', 'Intravenous Fluids', 'bottles', 100, 200)
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    generic_name = EXCLUDED.generic_name,
    category = EXCLUDED.category,
    unit = EXCLUDED.unit,
    minimum_stock_level = EXCLUDED.minimum_stock_level,
    reorder_level = EXCLUDED.reorder_level;

-- ------------------------------------------------------------------------------
-- Primary Health Centres (20 PHCs with realistic GPS coordinates)
-- ------------------------------------------------------------------------------
INSERT INTO phcs (id, district_id, name, code, address, latitude, longitude, location, total_beds, active_doctors, active_nurses, status) VALUES
-- Odisha - Khordha
('40000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'PHC Balipatna', 'OD-PHC-001', 'Balipatna Block, Khordha, Odisha - 752102', 20.183400, 85.952100, ST_SetSRID(ST_MakePoint(85.952100, 20.183400), 4326)::geography, 12, 2, 4, 'critical'),
('40000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001', 'PHC Jatani', 'OD-PHC-002', 'Jatani Main Road, Khordha, Odisha - 752050', 20.158500, 85.704200, ST_SetSRID(ST_MakePoint(85.704200, 20.158500), 4326)::geography, 16, 3, 5, 'healthy'),
('40000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000001', 'PHC Begunia', 'OD-PHC-003', 'Begunia Hospital Road, Khordha, Odisha - 752062', 20.203100, 85.478900, ST_SetSRID(ST_MakePoint(85.478900, 20.203100), 4326)::geography, 10, 2, 3, 'healthy'),

-- Odisha - Puri
('40000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000002', 'PHC Pipili', 'OD-PHC-004', 'Pipili Bazar, Puri District, Odisha - 752104', 20.116700, 85.833300, ST_SetSRID(ST_MakePoint(85.833300, 20.116700), 4326)::geography, 15, 3, 6, 'healthy'),
('40000000-0000-0000-0000-000000000005', '20000000-0000-0000-0000-000000000002', 'PHC Nimapada', 'OD-PHC-005', 'Nimapada Town, Puri, Odisha - 752106', 20.063100, 86.015200, ST_SetSRID(ST_MakePoint(86.015200, 20.063100), 4326)::geography, 14, 2, 4, 'at_risk'),
('40000000-0000-0000-0000-000000000006', '20000000-0000-0000-0000-000000000002', 'PHC Satyabadi', 'OD-PHC-006', 'Sakshigopal, Puri, Odisha - 752014', 19.952800, 85.827400, ST_SetSRID(ST_MakePoint(85.827400, 19.952800), 4326)::geography, 12, 2, 3, 'healthy'),

-- Odisha - Cuttack
('40000000-0000-0000-0000-000000000007', '20000000-0000-0000-0000-000000000003', 'PHC Salipur', 'OD-PHC-007', 'Salipur Block Road, Cuttack, Odisha - 754202', 20.485600, 86.002800, ST_SetSRID(ST_MakePoint(86.002800, 20.485600), 4326)::geography, 18, 3, 5, 'healthy'),
('40000000-0000-0000-0000-000000000008', '20000000-0000-0000-0000-000000000003', 'PHC Nischintakoili', 'OD-PHC-008', 'Nischintakoili, Cuttack, Odisha - 754207', 20.457800, 86.134500, ST_SetSRID(ST_MakePoint(86.134500, 20.457800), 4326)::geography, 10, 2, 3, 'healthy'),

-- West Bengal - South 24 Parganas
('40000000-0000-0000-0000-000000000009', '20000000-0000-0000-0000-000000000004', 'PHC Diamond Harbour', 'WB-PHC-001', 'Hospital Road, Diamond Harbour, South 24 Pgs, WB - 743331', 22.193100, 88.201400, ST_SetSRID(ST_MakePoint(88.201400, 22.193100), 4326)::geography, 20, 3, 7, 'at_risk'),
('40000000-0000-0000-0000-000000000010', '20000000-0000-0000-0000-000000000004', 'PHC Baruipur Rural', 'WB-PHC-002', 'Kulpi Road, Baruipur, South 24 Pgs, WB - 700144', 22.365400, 88.432100, ST_SetSRID(ST_MakePoint(88.432100, 22.365400), 4326)::geography, 16, 3, 5, 'healthy'),
('40000000-0000-0000-0000-000000000011', '20000000-0000-0000-0000-000000000004', 'PHC Canning', 'WB-PHC-003', 'Matla River Approach, Canning, South 24 Pgs, WB - 743329', 22.311200, 88.663400, ST_SetSRID(ST_MakePoint(88.663400, 22.311200), 4326)::geography, 14, 2, 4, 'at_risk'),

-- West Bengal - North 24 Parganas
('40000000-0000-0000-0000-000000000012', '20000000-0000-0000-0000-000000000005', 'PHC Habra Rural', 'WB-PHC-004', 'Jessore Road, Habra, North 24 Pgs, WB - 743263', 22.843100, 88.654200, ST_SetSRID(ST_MakePoint(88.654200, 22.843100), 4326)::geography, 15, 3, 5, 'healthy'),
('40000000-0000-0000-0000-000000000013', '20000000-0000-0000-0000-000000000005', 'PHC Barasat Rural', 'WB-PHC-005', 'Badu Road, Barasat, North 24 Pgs, WB - 700125', 22.721400, 88.482100, ST_SetSRID(ST_MakePoint(88.482100, 22.721400), 4326)::geography, 18, 4, 6, 'healthy'),
('40000000-0000-0000-0000-000000000014', '20000000-0000-0000-0000-000000000005', 'PHC Basirhat Rural', 'WB-PHC-006', 'Itinda Road, Basirhat, North 24 Pgs, WB - 743411', 22.658900, 88.894200, ST_SetSRID(ST_MakePoint(88.894200, 22.658900), 4326)::geography, 12, 2, 4, 'healthy'),

-- West Bengal - Howrah
('40000000-0000-0000-0000-000000000015', '20000000-0000-0000-0000-000000000006', 'PHC Uluberia Rural', 'WB-PHC-007', 'OT Road, Uluberia, Howrah, WB - 711315', 22.472100, 88.110200, ST_SetSRID(ST_MakePoint(88.110200, 22.472100), 4326)::geography, 16, 3, 5, 'healthy'),

-- Jharkhand - Ranchi
('40000000-0000-0000-0000-000000000016', '20000000-0000-0000-0000-000000000007', 'PHC Ormanjhi', 'JH-PHC-001', 'NH-33, Ormanjhi, Ranchi, Jharkhand - 835219', 23.481200, 85.478900, ST_SetSRID(ST_MakePoint(85.478900, 23.481200), 4326)::geography, 14, 2, 4, 'healthy'),
('40000000-0000-0000-0000-000000000017', '20000000-0000-0000-0000-000000000007', 'PHC Kanke', 'JH-PHC-002', 'Kanke Block Chowk, Ranchi, Jharkhand - 834006', 23.432100, 85.321400, ST_SetSRID(ST_MakePoint(85.321400, 23.432100), 4326)::geography, 15, 3, 5, 'healthy'),

-- Jharkhand - East Singhbhum
('40000000-0000-0000-0000-000000000018', '20000000-0000-0000-0000-000000000008', 'PHC Ghatshila', 'JH-PHC-003', 'College Road, Ghatshila, East Singhbhum, JH - 832303', 22.581200, 86.482100, ST_SetSRID(ST_MakePoint(86.482100, 22.581200), 4326)::geography, 16, 2, 5, 'at_risk'),
('40000000-0000-0000-0000-000000000019', '20000000-0000-0000-0000-000000000008', 'PHC Potka', 'JH-PHC-004', 'Potka Main Market, East Singhbhum, JH - 831002', 22.614200, 86.223400, ST_SetSRID(ST_MakePoint(86.223400, 22.614200), 4326)::geography, 10, 2, 3, 'healthy'),

-- Jharkhand - Dhanbad
('40000000-0000-0000-0000-000000000020', '20000000-0000-0000-0000-000000000009', 'PHC Govindpur', 'JH-PHC-005', 'GT Road, Govindpur, Dhanbad, Jharkhand - 828109', 23.834100, 86.521400, ST_SetSRID(ST_MakePoint(86.521400, 23.834100), 4326)::geography, 15, 3, 5, 'healthy')
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    code = EXCLUDED.code,
    address = EXCLUDED.address,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    location = EXCLUDED.location,
    total_beds = EXCLUDED.total_beds,
    active_doctors = EXCLUDED.active_doctors,
    active_nurses = EXCLUDED.active_nurses,
    status = EXCLUDED.status;
