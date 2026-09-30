-- ==============================================================================
-- SwasthyaGrid Database Schema
-- File: 003_indexes.sql
-- Description: Performance and geospatial indexing for SwasthyaGrid.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Geographic & Facility Lookups
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_districts_state_id ON districts(state_id);

CREATE INDEX IF NOT EXISTS idx_phcs_district_id ON phcs(district_id);
CREATE INDEX IF NOT EXISTS idx_phcs_status ON phcs(status);
CREATE INDEX IF NOT EXISTS idx_phcs_location ON phcs USING GIST (location);

-- ------------------------------------------------------------------------------
-- Medicine & Inventory Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_medicines_category ON medicines(category);

CREATE INDEX IF NOT EXISTS idx_inventory_phc_id ON inventory(phc_id);
CREATE INDEX IF NOT EXISTS idx_inventory_medicine_id ON inventory(medicine_id);
CREATE INDEX IF NOT EXISTS idx_inventory_phc_medicine ON inventory(phc_id, medicine_id);
CREATE INDEX IF NOT EXISTS idx_inventory_expiry_date ON inventory(expiry_date);

-- ------------------------------------------------------------------------------
-- Beds & Staff Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_beds_phc_id ON beds(phc_id);

CREATE INDEX IF NOT EXISTS idx_staff_phc_id ON staff(phc_id);
CREATE INDEX IF NOT EXISTS idx_staff_role ON staff(role);
CREATE INDEX IF NOT EXISTS idx_staff_is_active ON staff(is_active);

CREATE INDEX IF NOT EXISTS idx_attendance_staff_id ON attendance(staff_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(attendance_date);
CREATE INDEX IF NOT EXISTS idx_attendance_staff_date ON attendance(staff_id, attendance_date);

-- ------------------------------------------------------------------------------
-- Time-Series & Epidemiology Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_patient_visits_phc_id ON patient_visits(phc_id);
CREATE INDEX IF NOT EXISTS idx_patient_visits_visit_date ON patient_visits(visit_date);
CREATE INDEX IF NOT EXISTS idx_patient_visits_phc_date ON patient_visits(phc_id, visit_date);
CREATE INDEX IF NOT EXISTS idx_patient_visits_disease ON patient_visits(disease_category);

CREATE INDEX IF NOT EXISTS idx_medicine_consumption_phc_id ON medicine_consumption(phc_id);
CREATE INDEX IF NOT EXISTS idx_medicine_consumption_medicine_id ON medicine_consumption(medicine_id);
CREATE INDEX IF NOT EXISTS idx_medicine_consumption_date ON medicine_consumption(consumption_date);
CREATE INDEX IF NOT EXISTS idx_medicine_consumption_phc_med_date ON medicine_consumption(phc_id, medicine_id, consumption_date);

-- ------------------------------------------------------------------------------
-- AI Forecasts & Alerting Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_forecasts_phc_id ON forecasts(phc_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_medicine_id ON forecasts(medicine_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_date ON forecasts(forecast_date);
CREATE INDEX IF NOT EXISTS idx_forecasts_phc_med_date ON forecasts(phc_id, medicine_id, forecast_date);

CREATE INDEX IF NOT EXISTS idx_risk_alerts_phc_id ON risk_alerts(phc_id);
CREATE INDEX IF NOT EXISTS idx_risk_alerts_medicine_id ON risk_alerts(medicine_id);
CREATE INDEX IF NOT EXISTS idx_risk_alerts_status_severity ON risk_alerts(status, severity);
CREATE INDEX IF NOT EXISTS idx_risk_alerts_type ON risk_alerts(alert_type);

-- ------------------------------------------------------------------------------
-- Resource Redistribution & Emergency Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_resource_transfers_source ON resource_transfers(source_phc_id);
CREATE INDEX IF NOT EXISTS idx_resource_transfers_destination ON resource_transfers(destination_phc_id);
CREATE INDEX IF NOT EXISTS idx_resource_transfers_status ON resource_transfers(status);
CREATE INDEX IF NOT EXISTS idx_resource_transfers_medicine ON resource_transfers(medicine_id);

CREATE INDEX IF NOT EXISTS idx_emergency_events_district ON emergency_events(affected_district_id);
CREATE INDEX IF NOT EXISTS idx_emergency_events_status ON emergency_events(status);
CREATE INDEX IF NOT EXISTS idx_emergency_events_type ON emergency_events(emergency_type);

-- ------------------------------------------------------------------------------
-- Audit Log Indexes
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor ON audit_logs(actor_type, actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
