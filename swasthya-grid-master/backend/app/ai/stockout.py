from datetime import date, timedelta
from typing import Dict, Any, List
import math


class StockoutEngine:
    """
    Evaluates current inventory against forward demand projections to detect
    stock-outs, compute depletion trajectories, and assign explainable risk tiers.
    """

    @classmethod
    def evaluate_item_risk(
        cls,
        medicine_id: str,
        medicine_name: str,
        medicine_category: str,
        unit: str,
        current_stock: int,
        reserved_stock: int,
        daily_average_consumption: float,
        predicted_daily_demand: float,
        minimum_stock_level: int,
        reorder_level: int
    ) -> Dict[str, Any]:
        """
        Computes stockout horizon, risk score (0-100), risk tier, and human-readable explanation.
        """
        effective_demand = max(predicted_daily_demand, daily_average_consumption, 0.1)
        effective_available_stock = max(0, current_stock - reserved_stock)

        # Days of stock remaining
        days_remaining = round(effective_available_stock / effective_demand, 1)

        # Estimated stockout date
        stockout_date = None
        if days_remaining <= 60:
            stockout_date = date.today() + timedelta(days=max(0, int(math.floor(days_remaining))))

        # Risk Classification & Risk Score (0-100)
        if days_remaining <= 2.0 or current_stock <= minimum_stock_level:
            risk_level = "CRITICAL"
            # Linear scale from 85 to 100 for critical
            severity_factor = max(0.0, 1.0 - (days_remaining / 2.0))
            risk_score = round(85.0 + (15.0 * severity_factor), 2)
            explanation = (
                f"CRITICAL risk: Current available stock of {current_stock} {unit} covers only "
                f"{days_remaining} days of projected daily demand ({round(effective_demand, 1)} {unit}/day). "
                f"Stock is below the minimum safety threshold ({minimum_stock_level} {unit})."
            )
        elif days_remaining <= 5.0 or current_stock <= reorder_level:
            risk_level = "HIGH"
            severity_factor = max(0.0, 1.0 - ((days_remaining - 2.0) / 3.0))
            risk_score = round(65.0 + (20.0 * severity_factor), 2)
            explanation = (
                f"HIGH risk: Current stock ({current_stock} {unit}) is below the reorder point ({reorder_level} {unit}) "
                f"with {days_remaining} days of supply remaining."
            )
        elif days_remaining <= 10.0:
            risk_level = "MEDIUM"
            severity_factor = max(0.0, 1.0 - ((days_remaining - 5.0) / 5.0))
            risk_score = round(40.0 + (25.0 * severity_factor), 2)
            explanation = (
                f"MEDIUM risk: Stock level is approaching replenishment threshold with {days_remaining} days buffer."
            )
        else:
            risk_level = "LOW"
            risk_score = round(max(5.0, 35.0 - (days_remaining * 0.5)), 2)
            explanation = (
                f"LOW risk: Stock is healthy ({current_stock} {unit}) covering {days_remaining} days of projected demand."
            )

        return {
            "medicine_id": str(medicine_id),
            "medicine_name": medicine_name,
            "medicine_category": medicine_category,
            "unit": unit,
            "current_stock": current_stock,
            "reserved_stock": reserved_stock,
            "effective_available_stock": effective_available_stock,
            "predicted_daily_demand": round(effective_demand, 2),
            "days_of_stock_remaining": days_remaining,
            "minimum_stock_level": minimum_stock_level,
            "reorder_level": reorder_level,
            "estimated_stockout_date": stockout_date,
            "risk_score": min(100.0, max(0.0, risk_score)),
            "risk_level": risk_level,
            "explanation": explanation
        }
