@echo off
echo ==========================================
echo Random Forest Training
echo ==========================================
call venv\Scripts\activate
python model\train_model.py
pause
