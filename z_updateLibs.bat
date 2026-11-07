@echo off
setlocal

cd /d "%~dp0"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Update Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Setup complete.
endlocal