from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "weather_decision_tree.joblib"

FEATURES = [
    "temperature",
    "humidity",
    "precipitation",
    "cloud_cover",
    "wind_speed",
    "surface_pressure",
]

TARGET = "weather_class"


def weather_code_to_class(code):
    if pd.isna(code):
        return None

    try:
        code = int(code)
    except (ValueError, TypeError):
        return None

    if code in (0, 1):
        return "Clear"
    if code in (2, 3):
        return "Cloudy"
    if code in (51, 53, 55):
        return "Drizzle"
    if code in (61, 63, 65):
        return "Rain"

    return None


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}. "
            "Run: python model/train_model.py"
        )

    return joblib.load(MODEL_PATH)


def predict_category(model, values):
    row = pd.DataFrame([{
        "temperature": values.get("temperature"),
        "humidity": values.get("humidity"),
        "precipitation": values.get("precipitation"),
        "cloud_cover": values.get("cloud_cover"),
        "wind_speed": values.get("wind_speed"),
        "surface_pressure": values.get("surface_pressure"),
    }])

    return str(model.predict(row)[0])
