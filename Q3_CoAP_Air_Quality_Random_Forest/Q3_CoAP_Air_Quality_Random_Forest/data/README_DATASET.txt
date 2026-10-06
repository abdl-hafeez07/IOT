DATASET SETUP

1. Download the official Kaggle dataset:
   https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india

2. Extract the downloaded archive.

3. Find:
   city_day.csv

4. Copy city_day.csv into this folder:

   Q3_CoAP_Air_Quality_Random_Forest/data/

5. Final path must be:

   data/city_day.csv

The ZIP intentionally does not contain the full Kaggle dataset. The project code expects the official city_day.csv file to be downloaded by the student.

Required columns:
- PM2.5
- PM10
- NO2
- SO2
- O3
- AQI_Bucket

The training script normalizes common column spellings automatically.
