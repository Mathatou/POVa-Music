@echo off
setlocal

cd /d "%~dp0"

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 exit /b 1

echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Setup complete.
endlocal