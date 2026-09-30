from uuid import UUID
from datetime import date, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from app.models.phc import PHC
from app.models.bed import Bed
from app.models.staff import Staff
from app.models.attendance import Attendance
from app.models.inventory import Inventory
from app.models.medicine import Medicine
from app.models.patient_visit import PatientVisit
from app.schemas.health_metrics import PHCHealthMetricsResponse, MedicineStockStatus


class HealthMetricsService:
    @staticmethod
    async def compute_phc_metrics(db: AsyncSession, phc_id: UUID) -> PHCHealthMetricsResponse:
        """
        Computes non-AI operational resilience and load metrics for a given PHC.
        """
        # 1. Fetch PHC
        phc_result = await db.execute(select(PHC).where(PHC.id == phc_id))
        phc = phc_result.scalar_one_or_none()
        if not phc:
            raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

        # 2. Fetch Beds
        bed_result = await db.execute(select(Bed).where(Bed.phc_id == phc_id))
        bed = bed_result.scalar_one_or_none()
        
        total_beds = bed.total_beds if bed else phc.total_beds
        occupied_beds = bed.occupied_beds if bed else 0
        reserved_beds = bed.reserved_beds if bed else 0
        available_beds = bed.available_beds if bed else max(0, total_beds - occupied_beds - reserved_beds)
        
        occupancy_rate = round((occupied_beds / total_beds * 100.0), 2) if total_beds > 0 else 0.0

        # 3. Fetch Staff & Attendance
        staff_result = await db.execute(select(Staff).where(Staff.phc_id == phc_id))
        staff_list = staff_result.scalars().all()
        
        total_staff = len(staff_list)
        active_staff = sum(1 for s in staff_list if s.is_active)
        doctor_count = sum(1 for s in staff_list if s.role == "doctor" and s.is_active)
        nurse_count = sum(1 for s in staff_list if s.role == "nurse" and s.is_active)

        # Attendance today
        today = date.today()
        staff_ids = [s.id for s in staff_list]
        present_today = 0
        if staff_ids:
            att_result = await db.execute(
                select(func.count(Attendance.id))
                .where(
                    Attendance.staff_id.in_(staff_ids),
                    Attendance.attendance_date == today,
                    Attendance.status.in_(["present", "on_duty"])
                )
            )
            present_today = att_result.scalar() or 0
        
        staff_availability_rate = round((present_today / total_staff * 100.0), 2) if total_staff > 0 else 0.0

        # 4. Fetch Recent 7-day Patient Load
        seven_days_ago = today - timedelta(days=7)
        patient_visits_result = await db.execute(
            select(
                func.coalesce(func.sum(PatientVisit.patient_count), 0).label("total_patients"),
                func.coalesce(func.sum(PatientVisit.emergency_count), 0).label("total_emergencies")
            ).where(
                PatientVisit.phc_id == phc_id,
                PatientVisit.visit_date >= seven_days_ago
            )
        )
        patient_row = patient_visits_result.one()
        recent_7day_visits = int(patient_row.total_patients)
        recent_7day_emergencies = int(patient_row.total_emergencies)
        daily_avg_visits = round(recent_7day_visits / 7.0, 2)

        # 5. Fetch Inventory & Classify Stock Health
        inv_result = await db.execute(
            select(Inventory, Medicine)
            .join(Medicine, Inventory.medicine_id == Medicine.id)
            .where(Inventory.phc_id == phc_id)
        )
        inventory_rows = inv_result.all()

        total_meds = len(inventory_rows)
        critical_count = 0
        low_count = 0
        adequate_count = 0
        surplus_count = 0
        critical_medicines_list: List[MedicineStockStatus] = []

        for inv, med in inventory_rows:
            days_supply = None
            if float(inv.daily_average_consumption) > 0:
                days_supply = round(inv.quantity / float(inv.daily_average_consumption), 1)

            if inv.quantity <= med.minimum_stock_level:
                status_str = "critical"
                critical_count += 1
                critical_medicines_list.append(MedicineStockStatus(
                    medicine_id=med.id,
                    medicine_name=med.name,
                    category=med.category,
                    current_stock=inv.quantity,
                    minimum_stock_level=med.minimum_stock_level,
                    reorder_level=med.reorder_level,
                    days_of_supply_remaining=days_supply,
                    status="critical"
                ))
            elif inv.quantity <= med.reorder_level:
                status_str = "low"
                low_count += 1
            elif inv.quantity >= med.reorder_level * 2:
                status_str = "surplus"
                surplus_count += 1
            else:
                status_str = "adequate"
                adequate_count += 1

        availability_pct = round(((adequate_count + surplus_count) / total_meds * 100.0), 2) if total_meds > 0 else 0.0

        return PHCHealthMetricsResponse(
            phc_id=phc.id,
            phc_name=phc.name,
            phc_code=phc.code,
            status=phc.status,
            total_beds=total_beds,
            occupied_beds=occupied_beds,
            reserved_beds=reserved_beds,
            available_beds=available_beds,
            bed_occupancy_rate_pct=occupancy_rate,
            total_staff=total_staff,
            active_staff=active_staff,
            present_today=present_today,
            staff_availability_rate_pct=staff_availability_rate,
            doctor_count=doctor_count,
            nurse_count=nurse_count,
            recent_7day_total_visits=recent_7day_visits,
            recent_7day_daily_average_visits=daily_avg_visits,
            recent_7day_emergencies=recent_7day_emergencies,
            total_medicines_tracked=total_meds,
            critical_medicines_count=critical_count,
            low_stock_medicines_count=low_count,
            adequate_medicines_count=adequate_count,
            surplus_medicines_count=surplus_count,
            medicine_availability_pct=availability_pct,
            critical_medicines_list=critical_medicines_list
        )
