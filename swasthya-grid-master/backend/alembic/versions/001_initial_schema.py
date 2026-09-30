"""Initial database schema with PostGIS and 16 core tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-23 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable PostGIS and UUID extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. states
    op.create_table(
        'states',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('code', sa.String(10), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 3. districts
    op.create_table(
        'districts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('state_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('states.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(15), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 4. phcs
    op.create_table(
        'phcs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('district_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('districts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('code', sa.String(30), nullable=False, unique=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(9, 6), nullable=False),
        sa.Column('longitude', sa.Numeric(9, 6), nullable=False),
        sa.Column('location', geoalchemy2.Geography(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('total_beds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('active_doctors', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('active_nurses', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(20), nullable=False, server_default='healthy'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 5. medicines
    op.create_table(
        'medicines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('generic_name', sa.String(150), nullable=False),
        sa.Column('category', sa.String(80), nullable=False),
        sa.Column('unit', sa.String(30), nullable=False),
        sa.Column('minimum_stock_level', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('reorder_level', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 6. inventory
    op.create_table(
        'inventory',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('medicines.id', ondelete='CASCADE'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reserved_quantity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('daily_average_consumption', sa.Numeric(8, 2), nullable=False, server_default='0.00'),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('batch_number', sa.String(50), nullable=False),
        sa.Column('last_restocked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 7. beds
    op.create_table(
        'beds',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('total_beds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('occupied_beds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reserved_beds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 8. staff
    op.create_table(
        'staff',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('employee_code', sa.String(50), nullable=False, unique=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('specialization', sa.String(100), nullable=True),
        sa.Column('employment_type', sa.String(30), nullable=False, server_default='permanent'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('joined_at', sa.Date(), nullable=False)
    )

    # 9. attendance
    op.create_table(
        'attendance',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('staff_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('staff.id', ondelete='CASCADE'), nullable=False),
        sa.Column('attendance_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='present'),
        sa.Column('check_in', sa.Time(), nullable=True),
        sa.Column('check_out', sa.Time(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 10. patient_visits
    op.create_table(
        'patient_visits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('visit_date', sa.Date(), nullable=False),
        sa.Column('disease_category', sa.String(80), nullable=False),
        sa.Column('patient_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('emergency_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 11. medicine_consumption
    op.create_table(
        'medicine_consumption',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('medicines.id', ondelete='CASCADE'), nullable=False),
        sa.Column('consumption_date', sa.Date(), nullable=False),
        sa.Column('quantity_consumed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 12. forecasts
    op.create_table(
        'forecasts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('medicines.id', ondelete='CASCADE'), nullable=False),
        sa.Column('forecast_date', sa.Date(), nullable=False),
        sa.Column('predicted_demand', sa.Numeric(8, 2), nullable=False),
        sa.Column('lower_bound', sa.Numeric(8, 2), nullable=True),
        sa.Column('upper_bound', sa.Numeric(8, 2), nullable=True),
        sa.Column('confidence_score', sa.Numeric(5, 4), nullable=True),
        sa.Column('model_version', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 13. risk_alerts
    op.create_table(
        'risk_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('medicines.id', ondelete='SET NULL'), nullable=True),
        sa.Column('alert_type', sa.String(40), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('risk_score', sa.Numeric(5, 2), nullable=False),
        sa.Column('recommended_action', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 14. resource_transfers
    op.create_table(
        'resource_transfers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('source_phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('destination_phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('resource_type', sa.String(30), nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('medicines.id', ondelete='SET NULL'), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(30), nullable=False, server_default='recommended'),
        sa.Column('distance_km', sa.Numeric(8, 2), nullable=True),
        sa.Column('estimated_arrival_minutes', sa.Integer(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('approved_by', sa.String(100), nullable=True)
    )

    # 15. emergency_events
    op.create_table(
        'emergency_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('emergency_type', sa.String(40), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('affected_district_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('districts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 16. audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('actor_type', sa.String(50), nullable=False),
        sa.Column('actor_id', sa.String(100), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.String(100), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # 17. users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(30), nullable=False),
        sa.Column('state_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('states.id', ondelete='CASCADE'), nullable=True),
        sa.Column('district_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('districts.id', ondelete='CASCADE'), nullable=True),
        sa.Column('phc_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('phcs.id', ondelete='CASCADE'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('audit_logs')
    op.drop_table('emergency_events')
    op.drop_table('resource_transfers')
    op.drop_table('risk_alerts')
    op.drop_table('forecasts')
    op.drop_table('medicine_consumption')
    op.drop_table('patient_visits')
    op.drop_table('attendance')
    op.drop_table('staff')
    op.drop_table('beds')
    op.drop_table('inventory')
    op.drop_table('medicines')
    op.drop_table('phcs')
    op.drop_table('districts')
    op.drop_table('states')
