from pathlib import Path
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "historical_weather.csv"

URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=9.93&longitude=76.27"
    "&start_date=2023-01-01&end_date=2025-12-31"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation,"
    "cloud_cover,wind_speed_10m,surface_pressure,weather_code"
    "&timezone=Asia%2FKolkata"
)


def main():
    print("=" * 70)
    print("Downloading Kochi Historical Weather Dataset")
    print("=" * 70)

    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    data = response.json()

    if "hourly" not in data:
        raise RuntimeError(f"Unexpected API response: {data}")

    hourly = data["hourly"]

    df = pd.DataFrame({
        "time": hourly.get("time", []),
        "temperature": hourly.get("temperature_2m", []),
        "humidity": hourly.get("relative_humidity_2m", []),
        "precipitation": hourly.get("precipitation", []),
        "cloud_cover": hourly.get("cloud_cover", []),
        "wind_speed": hourly.get("wind_speed_10m", []),
        "surface_pressure": hourly.get("surface_pressure", []),
        "weather_code": hourly.get("weather_code", []),
    })

    df.to_csv(OUTPUT, index=False)

    print(f"Rows downloaded: {len(df)}")
    print(f"Saved to: {OUTPUT}")
    print("\nColumns:")
    print(list(df.columns))
    print("=" * 70)


if __name__ == "__main__":
    main()
