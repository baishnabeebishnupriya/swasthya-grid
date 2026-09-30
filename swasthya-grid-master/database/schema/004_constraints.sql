-- ==============================================================================
-- SwasthyaGrid Database Schema
-- File: 004_constraints.sql
-- Description: Business integrity, domain validation, and unique constraints.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- PHC Facility Integrity Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE phcs
    ADD CONSTRAINT chk_phc_status
        CHECK (status IN ('healthy', 'at_risk', 'critical')),
    ADD CONSTRAINT chk_phc_latitude
        CHECK (latitude BETWEEN -90.000000 AND 90.000000),
    ADD CONSTRAINT chk_phc_longitude
        CHECK (longitude BETWEEN -180.000000 AND 180.000000),
    ADD CONSTRAINT chk_phc_staff_beds
        CHECK (total_beds >= 0 AND active_doctors >= 0 AND active_nurses >= 0);

-- ------------------------------------------------------------------------------
-- Medicine Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE medicines
    ADD CONSTRAINT chk_medicines_stock_thresholds
        CHECK (minimum_stock_level >= 0 AND reorder_level >= 0);

-- ------------------------------------------------------------------------------
-- Inventory Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE inventory
    ADD CONSTRAINT chk_inventory_quantities
        CHECK (
            quantity >= 0 AND
            reserved_quantity >= 0 AND
            reserved_quantity <= quantity AND
            daily_average_consumption >= 0.00
        ),
    ADD CONSTRAINT uq_inventory_phc_medicine_batch
        UNIQUE (phc_id, medicine_id, batch_number);

-- ------------------------------------------------------------------------------
-- Bed Availability Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE beds
    ADD CONSTRAINT chk_beds_non_negative
        CHECK (
            total_beds >= 0 AND
            occupied_beds >= 0 AND
            reserved_beds >= 0 AND
            available_beds >= 0
        ),
    ADD CONSTRAINT chk_beds_capacity_limit
        CHECK (occupied_beds + reserved_beds <= total_beds),
    ADD CONSTRAINT chk_beds_available_formula
        CHECK (available_beds = total_beds - (occupied_beds + reserved_beds));

-- ------------------------------------------------------------------------------
-- Staff & Attendance Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE staff
    ADD CONSTRAINT chk_staff_role
        CHECK (role IN ('doctor', 'nurse', 'pharmacist', 'lab_technician', 'administrative', 'other')),
    ADD CONSTRAINT chk_staff_employment_type
        CHECK (employment_type IN ('permanent', 'contract', 'visiting', 'temporary'));

ALTER TABLE attendance
    ADD CONSTRAINT chk_attendance_status
        CHECK (status IN ('present', 'absent', 'leave', 'on_duty')),
    ADD CONSTRAINT uq_attendance_staff_date
        UNIQUE (staff_id, attendance_date);

-- ------------------------------------------------------------------------------
-- Patient Visits & Epidemiology Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE patient_visits
    ADD CONSTRAINT chk_patient_visits_disease_category
        CHECK (disease_category IN (
            'general', 'fever', 'dengue', 'malaria',
            'respiratory', 'diarrhea', 'dehydration', 'injury', 'other'
        )),
    ADD CONSTRAINT chk_patient_visits_counts
        CHECK (patient_count >= 0 AND emergency_count >= 0 AND emergency_count <= patient_count),
    ADD CONSTRAINT uq_patient_visits_phc_date_category
        UNIQUE (phc_id, visit_date, disease_category);

-- ------------------------------------------------------------------------------
-- Medicine Consumption Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE medicine_consumption
    ADD CONSTRAINT chk_medicine_consumption_qty
        CHECK (quantity_consumed >= 0),
    ADD CONSTRAINT uq_medicine_consumption_phc_med_date
        UNIQUE (phc_id, medicine_id, consumption_date);

-- ------------------------------------------------------------------------------
-- AI Forecasting & Alerting Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE forecasts
    ADD CONSTRAINT chk_forecasts_values
        CHECK (
            predicted_demand >= 0 AND
            lower_bound >= 0 AND
            upper_bound >= lower_bound AND
            confidence_score BETWEEN 0.0000 AND 1.0000
        ),
    ADD CONSTRAINT uq_forecasts_phc_med_date_version
        UNIQUE (phc_id, medicine_id, forecast_date, model_version);

ALTER TABLE risk_alerts
    ADD CONSTRAINT chk_risk_alerts_type
        CHECK (alert_type IN ('stockout', 'bed_shortage', 'staff_shortage', 'demand_surge', 'emergency')),
    ADD CONSTRAINT chk_risk_alerts_severity
        CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    ADD CONSTRAINT chk_risk_alerts_status
        CHECK (status IN ('open', 'acknowledged', 'resolved')),
    ADD CONSTRAINT chk_risk_alerts_score
        CHECK (risk_score BETWEEN 0.00 AND 100.00);

-- ------------------------------------------------------------------------------
-- Resource Transfers & Emergency Constraints
-- ------------------------------------------------------------------------------
ALTER TABLE resource_transfers
    ADD CONSTRAINT chk_resource_transfers_type
        CHECK (resource_type IN ('medicine', 'equipment', 'staff', 'other')),
    ADD CONSTRAINT chk_resource_transfers_status
        CHECK (status IN ('recommended', 'pending_approval', 'approved', 'in_transit', 'completed', 'cancelled')),
    ADD CONSTRAINT chk_resource_transfers_quantity
        CHECK (quantity > 0),
    ADD CONSTRAINT chk_resource_transfers_distinct_phcs
        CHECK (source_phc_id <> destination_phc_id),
    ADD CONSTRAINT chk_resource_transfers_distance
        CHECK (distance_km IS NULL OR distance_km >= 0.00),
    ADD CONSTRAINT chk_resource_transfers_duration
        CHECK (estimated_arrival_minutes IS NULL OR estimated_arrival_minutes >= 0);

ALTER TABLE emergency_events
    ADD CONSTRAINT chk_emergency_events_type
        CHECK (emergency_type IN ('disease_outbreak', 'flood', 'cyclone', 'heatwave', 'mass_casualty', 'other')),
    ADD CONSTRAINT chk_emergency_events_severity
        CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    ADD CONSTRAINT chk_emergency_events_status
        CHECK (status IN ('active', 'contained', 'concluded'));
