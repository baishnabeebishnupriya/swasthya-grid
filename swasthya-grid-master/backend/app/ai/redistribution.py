import math
from typing import Dict, Any, List, Optional
import pandas as pd


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS coordinates in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


class RedistributionOptimizer:
    """
    Recommends safe, proximity-optimized peer-to-peer resource rebalancing between
    surplus and deficit Primary Health Centres without endangering donor capacity.
    """

    @classmethod
    def recommend_transfers(
        cls,
        dest_phc_id: str,
        dest_phc_name: str,
        dest_lat: float,
        dest_lon: float,
        dest_stock_items: List[Dict[str, Any]],
        all_phc_inventory: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Scans network for medicines in critical/high deficit at dest_phc and pairs them
        with optimal nearby surplus donor nodes.
        """
        recommendations = []

        # Identify items in destination PHC needing replenishment
        for item in dest_stock_items:
            if item.get("risk_level") not in ["CRITICAL", "HIGH"]:
                continue

            med_id = item["medicine_id"]
            med_name = item["medicine_name"]
            med_unit = item.get("unit", "units")
            dest_stock = item["current_stock"]
            dest_reorder = item["reorder_level"]
            dest_daily = item["predicted_daily_demand"]

            target_deficit = max(100, int((dest_reorder * 1.5) - dest_stock))

            # Query all potential donor PHCs possessing this medicine
            candidates_df = all_phc_inventory[
                (all_phc_inventory["medicine_id"] == med_id) &
                (all_phc_inventory["phc_id"] != dest_phc_id)
            ].copy()

            if candidates_df.empty:
                continue

            candidate_evaluations = []
            for _, donor in candidates_df.iterrows():
                donor_stock = int(donor["quantity"])
                donor_reorder = int(donor["reorder_level"])
                donor_daily = float(donor["daily_average_consumption"])
                donor_lat = float(donor["latitude"])
                donor_lon = float(donor["longitude"])

                # Safety Buffer for donor: Reorder level + 7 days buffer
                donor_safety_buffer = donor_reorder + int(donor_daily * 7)
                available_surplus = max(0, donor_stock - donor_safety_buffer)

                if available_surplus < 50:
                    continue  # Do not compromise donor node

                distance_km = haversine_distance_km(dest_lat, dest_lon, donor_lat, donor_lon)
                eta_minutes = max(15, int(distance_km * 2.2 + 10))

                # Composite score: higher surplus, lower distance
                score = round(available_surplus / max(distance_km, 2.0), 2)

                candidate_evaluations.append({
                    "donor_phc_id": str(donor["phc_id"]),
                    "donor_phc_name": donor["phc_name"],
                    "donor_phc_code": donor["phc_code"],
                    "donor_stock": donor_stock,
                    "available_surplus": available_surplus,
                    "distance_km": distance_km,
                    "eta_minutes": eta_minutes,
                    "ranking_score": score
                })

            if not candidate_evaluations:
                continue

            # Rank candidate donors descending by score
            candidate_evaluations.sort(key=lambda x: x["ranking_score"], reverse=True)
            best_donor = candidate_evaluations[0]

            transfer_qty = min(target_deficit, best_donor["available_surplus"])

            reason = (
                f"{best_donor['donor_phc_name']} possesses {best_donor['available_surplus']} safe surplus {med_unit} "
                f"and is the optimal closest facility ({best_donor['distance_km']} km, ETA ~{best_donor['eta_minutes']} min) "
                f"to resolve {dest_phc_name}'s imminent {item['risk_level'].lower()} stockout."
            )

            recommendations.append({
                "medicine_id": str(med_id),
                "medicine_name": med_name,
                "unit": med_unit,
                "destination_phc_id": str(dest_phc_id),
                "destination_phc_name": dest_phc_name,
                "source_phc_id": best_donor["donor_phc_id"],
                "source_phc_name": best_donor["donor_phc_name"],
                "source_phc_code": best_donor["donor_phc_code"],
                "recommended_quantity": transfer_qty,
                "distance_km": best_donor["distance_km"],
                "estimated_arrival_minutes": best_donor["eta_minutes"],
                "destination_urgency": item["risk_level"],
                "reason": reason,
                "alternative_sources_count": len(candidate_evaluations) - 1
            })

        return recommendations
