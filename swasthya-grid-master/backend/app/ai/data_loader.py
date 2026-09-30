from typing import Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.medicine_consumption import MedicineConsumption
from app.models.patient_visit import PatientVisit
from app.models.inventory import Inventory
from app.models.phc import PHC
from app.models.medicine import Medicine
from app.models.bed import Bed
from app.models.staff import Staff
from app.models.attendance import Attendance
from app.models.district import District
from app.models.state import State


class DataLoader:
    """
    Extracts and structures historical database records into clean Pandas DataFrames.
    """

    @staticmethod
    async def load_consumption_data(db: AsyncSession, phc_id: Optional[str] = None) -> pd.DataFrame:
        """
        Loads historical medicine consumption time-series.
        """
        query = (
            select(
                MedicineConsumption.phc_id,
                MedicineConsumption.medicine_id,
                MedicineConsumption.consumption_date,
                MedicineConsumption.quantity_consumed,
                Medicine.name.label("medicine_name"),
                Medicine.category.label("medicine_category"),
                PHC.name.label("phc_name"),
                PHC.code.label("phc_code")
            )
            .join(Medicine, MedicineConsumption.medicine_id == Medicine.id)
            .join(PHC, MedicineConsumption.phc_id == PHC.id)
        )
        if phc_id:
            query = query.where(MedicineConsumption.phc_id == phc_id)

        query = query.order_by(MedicineConsumption.consumption_date.asc())
        result = await db.execute(query)
        rows = result.mappings().all()
        
        if not rows:
            return pd.DataFrame(columns=[
                "phc_id", "medicine_id", "consumption_date", "quantity_consumed",
                "medicine_name", "medicine_category", "phc_name", "phc_code"
            ])

        df = pd.DataFrame(rows)
        df["consumption_date"] = pd.to_datetime(df["consumption_date"])
        df["quantity_consumed"] = pd.to_numeric(df["quantity_consumed"], errors="coerce").fillna(0)
        return df

    @staticmethod
    async def load_patient_visits_data(db: AsyncSession, phc_id: Optional[str] = None) -> pd.DataFrame:
        """
        Loads historical aggregated patient visit data.
        """
        query = select(
            PatientVisit.phc_id,
            PatientVisit.visit_date,
            PatientVisit.disease_category,
            PatientVisit.patient_count,
            PatientVisit.emergency_count
        )
        if phc_id:
            query = query.where(PatientVisit.phc_id == phc_id)

        query = query.order_by(PatientVisit.visit_date.asc())
        result = await db.execute(query)
        rows = result.mappings().all()

        if not rows:
            return pd.DataFrame(columns=[
                "phc_id", "visit_date", "disease_category", "patient_count", "emergency_count"
            ])

        df = pd.DataFrame(rows)
        df["visit_date"] = pd.to_datetime(df["visit_date"])
        return df

    @staticmethod
    async def load_inventory_snapshot(db: AsyncSession, phc_id: Optional[str] = None) -> pd.DataFrame:
        """
        Loads current inventory snapshot with medicine reference thresholds.
        """
        query = (
            select(
                Inventory.id.label("inventory_id"),
                Inventory.phc_id,
                Inventory.medicine_id,
                Inventory.quantity,
                Inventory.reserved_quantity,
                Inventory.daily_average_consumption,
                Inventory.expiry_date,
                Inventory.batch_number,
                Medicine.name.label("medicine_name"),
                Medicine.category.label("medicine_category"),
                Medicine.unit.label("unit"),
                Medicine.minimum_stock_level,
                Medicine.reorder_level,
                PHC.name.label("phc_name"),
                PHC.code.label("phc_code"),
                PHC.latitude,
                PHC.longitude,
                PHC.status.label("phc_status")
            )
            .join(Medicine, Inventory.medicine_id == Medicine.id)
            .join(PHC, Inventory.phc_id == PHC.id)
        )
        if phc_id:
            query = query.where(Inventory.phc_id == phc_id)

        result = await db.execute(query)
        rows = result.mappings().all()

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        df["daily_average_consumption"] = pd.to_numeric(df["daily_average_consumption"], errors="coerce").fillna(0.0)
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        return df

    @staticmethod
    async def load_all_phcs_with_capacity(db: AsyncSession) -> pd.DataFrame:
        """
        Loads all PHC facility metadata, bed occupancy, doctor/nurse headcount, and coordinates.
        """
        query = (
            select(
                PHC.id.label("phc_id"),
                PHC.name.label("phc_name"),
                PHC.code.label("phc_code"),
                PHC.latitude,
                PHC.longitude,
                PHC.status.label("status"),
                PHC.total_beds,
                PHC.active_doctors,
                PHC.active_nurses,
                District.name.label("district_name"),
                State.name.label("state_name"),
                Bed.occupied_beds,
                Bed.reserved_beds,
                Bed.available_beds
            )
            .join(District, PHC.district_id == District.id)
            .join(State, District.state_id == State.id)
            .outerjoin(Bed, PHC.id == Bed.phc_id)
        )
        result = await db.execute(query)
        rows = result.mappings().all()
        df = pd.DataFrame(rows)
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        df["occupied_beds"] = pd.to_numeric(df["occupied_beds"], errors="coerce").fillna(0)
        df["available_beds"] = pd.to_numeric(df["available_beds"], errors="coerce").fillna(df["total_beds"])
        return df
