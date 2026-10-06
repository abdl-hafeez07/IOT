# Q3 - CoAP-Based Air Quality Monitoring and Random Forest Classification

## Objective

Develop a CoAP-based air-quality monitoring and classification system for Kochi.

Flow:

Air Quality API -> CoAP Server -> CoAP Client -> Dashboard -> Random Forest Classification

## Parameters

The system uses:

- PM2.5
- PM10
- NO2
- SO2
- O3

The live data source is the Open-Meteo Air Quality API for Kochi:

https://air-quality-api.open-meteo.com/v1/air-quality?latitude=9.93&longitude=76.27&current=pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,ozone

The historical training dataset is the Kaggle Air Quality Data in India dataset:

https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india

Required training file:

city_day.csv

## Project Structure

Q3_CoAP_Air_Quality_Random_Forest/
|
|-- coap/
|   |-- coap_server.py
|   |-- coap_client.py
|
|-- dashboard/
|   |-- app.py
|   |-- templates/
|       |-- index.html
|   |-- static/
|       |-- style.css
|
|-- model/
|   |-- train_model.py
|   |-- model_utils.py
|
|-- data/
|   |-- README_DATASET.txt
|   |-- city_day.csv              <-- put downloaded Kaggle file here
|
|-- scripts/
|   |-- run_all_windows.bat
|   |-- run_training.bat
|   |-- test_coap_client.bat
|
|-- sample_output/
|   |-- coap_server_output.txt
|   |-- coap_client_output.txt
|
|-- exam_answer/
|   |-- ready_to_write_answer.txt
|
|-- requirements.txt
|-- README.md

## 1. Install Python

Recommended: Python 3.10 or 3.11.

Check:

python --version

## 2. Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

## 3. Install Packages

pip install -r requirements.txt

## 4. Download the Kaggle Dataset

Download the official "Air Quality Data in India" dataset and extract city_day.csv.

Place it here:

data/city_day.csv

Do not rename the file.

The training program uses:

PM2.5 -> pm2_5
PM10  -> pm10
NO2   -> no2
SO2   -> so2
O3    -> o3
Target -> AQI_Bucket

The program also handles common alternate spellings such as PM2.5, NO2, SO2, etc.

## 5. Train Random Forest

Run:

python model/train_model.py

This creates:

model/air_quality_random_forest.joblib

The model is trained only from rows where the five required features and AQI_Bucket are available.

The program prints:
- number of training rows
- class distribution
- test accuracy
- classification report
- saved model location

## 6. Start CoAP Server

Open Terminal 1:

python coap/coap_server.py

The server listens on:

coap://127.0.0.1:5683/air-quality

When the client sends GET /air-quality, the server retrieves the current Kochi values from Open-Meteo and returns them as JSON.

## 7. Test CoAP Client

Open Terminal 2:

python coap/coap_client.py

The client sends a CoAP GET request to:

coap://127.0.0.1:5683/air-quality

It prints the received PM2.5, PM10, NO2, SO2 and O3 values.

## 8. Start Dashboard

Open Terminal 3:

python dashboard/app.py

Open:

http://127.0.0.1:5000

The dashboard calls the CoAP client internally. Therefore the data path remains:

Open-Meteo -> CoAP Server -> CoAP Client -> Dashboard

The dashboard then passes the five values to the Random Forest model and displays the predicted AQI_Bucket.

## 9. Dashboard Features

The dashboard displays:

- Kochi location
- PM2.5
- PM10
- NO2
- SO2
- O3
- Random Forest predicted AQI category
- Last update time
- Data source
- CoAP flow

The page automatically refreshes the live reading every 60 seconds.

## 10. Troubleshooting

### "city_day.csv not found"

Put the Kaggle file at:

data/city_day.csv

Then run:

python model/train_model.py

### "Model file not found"

Run the training step before starting the dashboard:

python model/train_model.py

### CoAP client cannot connect

Make sure the CoAP server is running first:

python coap/coap_server.py

Then test:

python coap/coap_client.py

### Port 5683 already in use

Change COAP_PORT in coap/coap_server.py and coap/coap_client.py to the same unused port.

### API error

Check internet connectivity and try the Open-Meteo API URL in a browser.

## Important Academic Note

The Open-Meteo API supplies current air-quality model data. The Random Forest is trained from historical CPCB/India air-quality records in city_day.csv. These are different data sources.

The classification output is the prediction of the trained Random Forest model; it is not a direct CPCB AQI value.

## Reference Links

Open-Meteo Air Quality API:
https://open-meteo.com/en/docs/air-quality-api

Kaggle dataset:
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india

CPCB live air-quality portal:
https://app.cpcbccr.com/
