@echo off
echo ==========================================
echo Downloading historical data
echo ==========================================
call venv\Scripts\activate
python data\download_historical.py

echo.
echo ==========================================
echo Training Decision Tree
echo ==========================================
python model\train_model.py
pause
