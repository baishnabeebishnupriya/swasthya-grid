import json
from pathlib import Path
from typing import Optional, Dict, Any
import joblib

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


class ModelRegistry:
    """
    Manages persistence, versioning, and retrieval of trained forecasting models and evaluation logs.
    """

    MODEL_FILENAME = "demand_forecast_model.joblib"
    METADATA_FILENAME = "metadata.json"

    @classmethod
    def save_model(
        cls,
        model: Any,
        version: str,
        metrics: Dict[str, Any],
        artifact_dir: Optional[Path] = None
    ) -> Path:
        target_dir = artifact_dir or ARTIFACTS_DIR
        target_dir.mkdir(parents=True, exist_ok=True)

        model_path = target_dir / cls.MODEL_FILENAME
        metadata_path = target_dir / cls.METADATA_FILENAME

        # Save model weights
        joblib.dump(model, model_path)

        # Save metadata and evaluation metrics
        metadata = {
            "model_version": version,
            "evaluation_metrics": metrics
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return model_path

    @classmethod
    def load_model(cls, artifact_dir: Optional[Path] = None) -> Optional[Any]:
        target_dir = artifact_dir or ARTIFACTS_DIR
        model_path = target_dir / cls.MODEL_FILENAME
        if model_path.exists():
            try:
                return joblib.load(model_path)
            except Exception:
                return None
        return None

    @classmethod
    def load_metrics(cls, artifact_dir: Optional[Path] = None) -> Dict[str, Any]:
        target_dir = artifact_dir or ARTIFACTS_DIR
        metadata_path = target_dir / cls.METADATA_FILENAME
        if metadata_path.exists():
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
