from pathlib import Path
import sys

import joblib
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

sys.path.insert(0, str(Path(__file__).resolve().parent))

from model_utils import (
    FEATURES,
    TARGET,
    MODEL_PATH,
    weather_code_to_class,
)

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "historical_weather.csv"


def main():
    print("=" * 70)
    print("Decision Tree Training - Kochi Weather Classification")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"\nERROR: Dataset not found:\n{DATA_PATH}")
        print("\nRun first:")
        print("python data/download_historical.py")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)

    required = FEATURES + ["weather_code"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        print("ERROR: Missing columns:", missing)
        sys.exit(1)

    # Convert weather_code into the required target classes.
    df[TARGET] = df["weather_code"].apply(weather_code_to_class)

    # Keep only Clear, Cloudy, Drizzle and Rain.
    df = df.dropna(subset=[TARGET]).copy()

    for feature in FEATURES:
        df[feature] = pd.to_numeric(df[feature], errors="coerce")

    # Remove rows with no usable input features.
    df = df.dropna(subset=FEATURES, how="all")

    print(f"Rows used: {len(df)}")
    print("\nWeather class distribution:")
    print(df[TARGET].value_counts())

    X = df[FEATURES]
    y = df[TARGET]

    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=stratify,
    )

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DecisionTreeClassifier(
            random_state=42,
            max_depth=8,
            min_samples_leaf=5,
            class_weight="balanced",
        )),
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")
    print("\nInput Features:")
    for feature in FEATURES:
        print("-", feature)

    print("Target:", TARGET)
    print("=" * 70)


if __name__ == "__main__":
    main()
