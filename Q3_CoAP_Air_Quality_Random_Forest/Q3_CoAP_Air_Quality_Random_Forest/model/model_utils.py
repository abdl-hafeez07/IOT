from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "air_quality_random_forest.joblib"

FEATURES = ["pm2_5", "pm10", "no2", "so2", "o3"]
TARGET = "AQI_Bucket"


def normalize_column_name(name):
    text = str(name).strip().lower()
    replacements = {
        "pm2.5": "pm2_5",
        "pm2_5": "pm2_5",
        "pm10": "pm10",
        "no2": "no2",
        "so2": "so2",
        "o3": "o3",
        "aqi_bucket": "AQI_Bucket",
    }
    return replacements.get(text, text)


def prepare_dataframe(df):
    renamed = {}
    for col in df.columns:
        normalized = normalize_column_name(col)
        renamed[col] = normalized

    df = df.rename(columns=renamed)

    # Keep the first matching column if duplicate normalized names occur.
    df = df.loc[:, ~df.columns.duplicated()]

    return df


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}. "
            "Run: python model/train_model.py"
        )
    return joblib.load(MODEL_PATH)


def predict_category(model, values):
    row = pd.DataFrame([{
        "pm2_5": values.get("pm2_5"),
        "pm10": values.get("pm10"),
        "no2": values.get("no2"),
        "so2": values.get("so2"),
        "o3": values.get("o3"),
    }])

    prediction = model.predict(row)[0]
    return str(prediction)
