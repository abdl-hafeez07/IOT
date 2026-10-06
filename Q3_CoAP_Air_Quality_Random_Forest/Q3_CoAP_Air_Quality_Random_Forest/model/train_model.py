from pathlib import Path
import sys

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Allow importing model_utils when this file is run as:
# python model/train_model.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

from model_utils import FEATURES, TARGET, prepare_dataframe, MODEL_PATH

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "city_day.csv"


def main():
    print("=" * 70)
    print("Random Forest Training - Air Quality Classification")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"\nERROR: Dataset not found:\n{DATA_PATH}")
        print("\nDownload city_day.csv from the official Kaggle dataset and")
        print("place it in the data folder.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    df = prepare_dataframe(df)

    print(f"Dataset rows: {len(df)}")
    print(f"Dataset columns: {len(df.columns)}")

    required = FEATURES + [TARGET]
    missing = [col for col in required if col not in df.columns]

    if missing:
        print("\nERROR: Missing required columns:", missing)
        print("Available columns:", list(df.columns))
        sys.exit(1)

    work = df[required].copy()

    for feature in FEATURES:
        work[feature] = pd.to_numeric(work[feature], errors="coerce")

    work[TARGET] = work[TARGET].astype("string").str.strip()
    work = work.dropna(subset=[TARGET])

    # Remove rows where every sensor feature is missing.
    work = work.dropna(subset=FEATURES, how="all")

    print(f"Rows used for training/testing: {len(work)}")
    print("\nClass distribution:")
    print(work[TARGET].value_counts())

    X = work[FEATURES]
    y = work[TARGET]

    # Stratified split is used only when every class has at least 2 samples.
    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=stratify
    )

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        ))
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"\nModel saved to:\n{MODEL_PATH}")
    print("\nFeatures:", FEATURES)
    print("Target:", TARGET)
    print("=" * 70)


if __name__ == "__main__":
    main()
