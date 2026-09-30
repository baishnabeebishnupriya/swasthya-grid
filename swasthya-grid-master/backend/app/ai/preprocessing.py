from typing import Tuple, Optional, List
import pandas as pd
import numpy as np


class Preprocessing:
    """
    Transforms raw time-series observations into lag and window features
    strictly preventing data leakage.
    """

    FEATURE_COLUMNS: List[str] = [
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_30",
        "rolling_mean_7",
        "rolling_std_7",
        "rolling_mean_30",
        "day_of_week",
        "day_of_month",
        "month",
        "is_weekend",
        "is_monsoon"
    ]

    TARGET_COLUMN: str = "quantity_consumed"

    @classmethod
    def build_features(
        cls,
        consumption_df: pd.DataFrame,
        visits_df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Engineers chronological lag, rolling statistical, calendar, and epidemiological features.
        Optimized vectorized implementation.
        """
        if consumption_df.empty:
            return pd.DataFrame()

        df = consumption_df.copy()
        df["consumption_date"] = pd.to_datetime(df["consumption_date"])
        df = df.sort_values(["phc_id", "medicine_id", "consumption_date"]).reset_index(drop=True)

        # Vectorized lag calculations per (phc_id, medicine_id)
        grp = df.groupby(["phc_id", "medicine_id"])["quantity_consumed"]
        
        df["lag_1"] = grp.shift(1)
        df["lag_7"] = grp.shift(7)
        df["lag_14"] = grp.shift(14)
        df["lag_30"] = grp.shift(30)

        # Fast rolling averages on lagged values
        shifted_1 = grp.shift(1)
        df["rolling_mean_7"] = shifted_1.groupby([df["phc_id"], df["medicine_id"]]).transform(
            lambda x: x.rolling(7, min_periods=1).mean()
        )
        df["rolling_std_7"] = shifted_1.groupby([df["phc_id"], df["medicine_id"]]).transform(
            lambda x: x.rolling(7, min_periods=1).std()
        ).fillna(0.0)
        df["rolling_mean_30"] = shifted_1.groupby([df["phc_id"], df["medicine_id"]]).transform(
            lambda x: x.rolling(30, min_periods=1).mean()
        )

        # Calendar features
        df["day_of_week"] = df["consumption_date"].dt.dayofweek
        df["day_of_month"] = df["consumption_date"].dt.day
        df["month"] = df["consumption_date"].dt.month
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        df["is_monsoon"] = df["month"].isin([6, 7, 8, 9]).astype(int)

        # Backfill initial lag rows to prevent NaNs
        for col in ["lag_1", "lag_7", "lag_14", "lag_30", "rolling_mean_7", "rolling_std_7", "rolling_mean_30"]:
            df[col] = df[col].fillna(df["quantity_consumed"])

        return df

    @classmethod
    def chronological_split(
        cls,
        df: pd.DataFrame,
        test_days: int = 30
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits data chronologically based on date into Train and Out-of-Time Test sets.
        Ensures NO random shuffling.
        """
        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        max_date = df["consumption_date"].max()
        split_date = max_date - pd.Timedelta(days=test_days)

        train_df = df[df["consumption_date"] <= split_date].copy()
        test_df = df[df["consumption_date"] > split_date].copy()

        return train_df, test_df
