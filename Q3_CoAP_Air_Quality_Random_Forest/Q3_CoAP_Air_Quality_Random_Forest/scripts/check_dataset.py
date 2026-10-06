from pathlib import Path
import pandas as pd

path = Path("data/city_day.csv")

if not path.exists():
    print("city_day.csv not found in data/")
else:
    df = pd.read_csv(path, nrows=5)
    print("Dataset found.")
    print("Columns:")
    for col in df.columns:
        print(" -", col)
