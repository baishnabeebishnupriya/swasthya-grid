import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure backend root in python path
backend_root = Path(__file__).resolve().parent.parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.ai.preprocessing import Preprocessing
from app.ai.forecasting import DemandForecaster
from app.ai.model_registry import ModelRegistry


def generate_synthetic_training_data() -> pd.DataFrame:
    """
    Generates deterministic 180-day time-series data mirroring Phase 1 PostgreSQL schema.
    """
    records = []
    base_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=180)
    for phc_idx in range(1, 21):
        for med_idx in range(1, 16):
            base_qty = 20 if med_idx != 2 else 35
            for d in range(180):
                c_date = base_date + pd.Timedelta(days=d)
                noise = (hash(f"{phc_idx}_{med_idx}_{d}") % 8)
                # Spike for Balipatna (PHC 1) ORS (Med 2) in last 20 days
                spike = 25 if (phc_idx == 1 and med_idx == 2 and d >= 160) else 0
                records.append({
                    "phc_id": f"40000000-0000-0000-0000-0000000000{phc_idx:02d}",
                    "medicine_id": f"30000000-0000-0000-0000-0000000000{med_idx:02d}",
                    "consumption_date": c_date,
                    "quantity_consumed": base_qty + noise + spike,
                    "medicine_name": f"Medicine-{med_idx}",
                    "medicine_category": "Essential",
                    "phc_name": f"PHC-{phc_idx}",
                    "phc_code": f"PHC-{phc_idx:03d}"
                })
    return pd.DataFrame(records)


def train_forecasting_pipeline():
    print("=" * 70)
    print("SWASTHYAGRID AI DEMAND FORECASTING TRAINING & EVALUATION PIPELINE")
    print("=" * 70)

    # 1. Load Data
    print("\n[Step 1/4] Loading Historical Medicine Consumption Records...")
    df = generate_synthetic_training_data()
    print(f"  Loaded {len(df)} historical observations (180 days across 20 PHCs and 15 medicines).")

    # 2. Preprocess & Feature Engineering
    print("\n[Step 2/4] Engineering Lag, Rolling Window, and Calendar Features...")
    featured_df = Preprocessing.build_features(df)
    print(f"  Engineered feature matrix: {featured_df.shape[0]} rows, {len(Preprocessing.FEATURE_COLUMNS)} features.")

    # 3. Chronological Train / Test Split
    print("\n[Step 3/4] Performing Chronological Out-of-Time Train/Test Split (No Shuffling)...")
    train_df, test_df = Preprocessing.chronological_split(featured_df, test_days=30)
    print(f"  Train Set: {len(train_df)} observations (Dates <= {train_df['consumption_date'].max().date()})")
    print(f"  Test Set:  {len(test_df)} observations (Dates > {train_df['consumption_date'].max().date()})")

    # 4. Model Evaluation & Comparison
    print("\n[Step 4/4] Evaluating Baseline vs. Machine Learning Regressor...")
    forecaster = DemandForecaster()
    evaluation = forecaster.evaluate(train_df, test_df)

    print("\n" + "-" * 70)
    print("EVALUATION RESULTS (Out-of-Time Test Set):")
    print(f"  1. Baseline (7-Day Rolling Moving Average):")
    print(f"     - Mean Absolute Error (MAE):       {evaluation['baseline']['mae']}")
    print(f"     - Root Mean Squared Error (RMSE):    {evaluation['baseline']['rmse']}")
    print(f"     - Mean Abs Percentage Error (MAPE): {evaluation['baseline']['mape_pct']}%")
    print(f"  2. Machine Learning Model ({evaluation['ml_model']['name']}):")
    print(f"     - Mean Absolute Error (MAE):       {evaluation['ml_model']['mae']}")
    print(f"     - Root Mean Squared Error (RMSE):    {evaluation['ml_model']['rmse']}")
    print(f"     - Mean Abs Percentage Error (MAPE): {evaluation['ml_model']['mape_pct']}%")
    print("-" * 70)
    print(f"  >>> Selected Best Performing Approach: {evaluation['best_performing_model']} <<<")

    # 5. Fit on full data and save
    print("\nSaving trained model artifact and evaluation metadata...")
    forecaster.fit(featured_df)
    print("  Model saved to: backend/app/ai/artifacts/demand_forecast_model.joblib")
    print("  Metadata saved to: backend/app/ai/artifacts/metadata.json")
    print("=" * 70)
    return evaluation


if __name__ == "__main__":
    train_forecasting_pipeline()
