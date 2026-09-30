from typing import Dict, Any, List


class ResilienceScoringEngine:
    """
    Computes an explainable 0-100 PHC Resilience & Resource Capacity Score
    based on normalized operational sub-components.
    """

    WEIGHTS = {
        "medicine_availability": 0.30,
        "bed_availability": 0.20,
        "staff_availability": 0.20,
        "demand_pressure": 0.20,
        "emergency_readiness": 0.10
    }

    @classmethod
    def calculate_resilience(
        cls,
        phc_id: str,
        phc_name: str,
        inventory_items: List[Dict[str, Any]],
        total_beds: int,
        available_beds: int,
        active_doctors: int,
        active_nurses: int,
        staff_present_count: int,
        total_staff_count: int,
        recent_daily_visits: float,
        baseline_daily_visits: float,
        active_district_emergencies: int
    ) -> Dict[str, Any]:
        """
        Computes the weighted composite score and per-component breakdowns.
        """
        # 1. Medicine Availability Score (0 - 100)
        total_meds = len(inventory_items)
        if total_meds > 0:
            healthy_meds = sum(
                1 for item in inventory_items
                if item.get("risk_level") in ["LOW", "MEDIUM"]
            )
            medicine_score = (healthy_meds / total_meds) * 100.0
        else:
            medicine_score = 50.0

        # 2. Bed Availability Score (0 - 100)
        if total_beds > 0:
            bed_score = (available_beds / total_beds) * 100.0
        else:
            bed_score = 50.0

        # 3. Staff Readiness Score (0 - 100)
        if total_staff_count > 0:
            attendance_ratio = min(1.0, staff_present_count / max(1, total_staff_count))
            clinician_factor = min(1.0, (active_doctors * 0.3 + active_nurses * 0.15))
            staff_score = (attendance_ratio * 60.0) + (clinician_factor * 40.0)
        else:
            staff_score = 50.0

        # 4. Demand Pressure Score (0 - 100, where 100 = stable baseline, lower = high surge stress)
        if baseline_daily_visits > 0:
            surge_ratio = recent_daily_visits / baseline_daily_visits
            if surge_ratio <= 1.0:
                demand_score = 100.0
            elif surge_ratio >= 2.5:
                demand_score = 20.0
            else:
                demand_score = max(20.0, 100.0 - ((surge_ratio - 1.0) / 1.5 * 80.0))
        else:
            demand_score = 80.0

        # 5. Emergency Readiness Score (0 - 100)
        if active_district_emergencies == 0:
            emergency_score = 100.0
        elif active_district_emergencies == 1:
            emergency_score = 65.0
        else:
            emergency_score = 35.0

        # Clamp all components strictly to [0, 100]
        comp_m = max(0.0, min(100.0, medicine_score))
        comp_b = max(0.0, min(100.0, bed_score))
        comp_s = max(0.0, min(100.0, staff_score))
        comp_d = max(0.0, min(100.0, demand_score))
        comp_e = max(0.0, min(100.0, emergency_score))

        # Composite Weighted Score
        resilience_score = round(
            (comp_m * cls.WEIGHTS["medicine_availability"]) +
            (comp_b * cls.WEIGHTS["bed_availability"]) +
            (comp_s * cls.WEIGHTS["staff_availability"]) +
            (comp_d * cls.WEIGHTS["demand_pressure"]) +
            (comp_e * cls.WEIGHTS["emergency_readiness"]),
            1
        )

        # Status Classification
        if resilience_score >= 80.0:
            status = "HEALTHY"
            explanation = "Facility exhibits strong resilience with balanced supply buffer and manageable clinical load."
        elif resilience_score >= 60.0:
            status = "AT_RISK"
            explanation = "Facility capacity is constrained; heightened demand or isolated supply dips detected."
        else:
            status = "CRITICAL"
            explanation = "Critical resilience deficit: severe inventory depletion, bed saturations, or surge pressure."

        return {
            "phc_id": str(phc_id),
            "phc_name": phc_name,
            "resilience_score": resilience_score,
            "status": status,
            "components": {
                "medicine_availability": round(comp_m, 1),
                "bed_availability": round(comp_b, 1),
                "staff_availability": round(comp_s, 1),
                "demand_stability": round(comp_d, 1),
                "emergency_readiness": round(comp_e, 1)
            },
            "weights": cls.WEIGHTS,
            "explanation": explanation
        }
