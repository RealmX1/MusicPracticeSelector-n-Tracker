@echo off
REM Music Practice Tracker Build Script for Windows
REM This script builds the application for Windows

echo ===================================
echo Music Practice Tracker Build Script
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [INFO] Installing requirements...
pip install -r requirements.txt

REM Install PyInstaller
echo [INFO] Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo [INFO] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
if "%1"=="--onedir" (
    echo [INFO] Building as directory bundle...
    pyinstaller ^
        --name MusicPracticeTracker ^
        --windowed ^
        --add-data "config.json;." ^
        --add-data "requirements.txt;." ^
        --add-data "README.md;." ^
        --add-data "license.md;." ^
        --hidden-import pandas ^
        --hidden-import reportlab ^
        --hidden-import pypdfium2 ^
        --hidden-import PIL ^
        --hidden-import tkinter ^
        --clean ^
        app.py
) else (
    echo [INFO] Building as single executable...
    pyinstaller ^
        --name MusicPracticeTracker ^
        --onefile ^
        --windowed ^
        --add-data "config.json;." ^
        --add-data "requirements.txt;." ^
        --add-data "README.md;." ^
        --add-data "license.md;." ^
        --hidden-import pandas ^
        --hidden-import reportlab ^
        --hidden-import pypdfium2 ^
        --hidden-import PIL ^
        --hidden-import tkinter ^
        --clean ^
        app.py
)

REM Check if build was successful
if exist "dist\MusicPracticeTracker.exe" (
    echo [OK] Build completed successfully!
    echo [OK] Output location: dist\
    
    REM Create a zip file for distribution
    echo [INFO] Creating distribution archive...
    cd dist
    powershell -command "Compress-Archive -Path * -DestinationPath MusicPracticeTracker-Windows.zip -Force"
    cd ..
    echo [OK] Distribution archive created: dist\MusicPracticeTracker-Windows.zip
) else if exist "dist\MusicPracticeTracker" (
    echo [OK] Build completed successfully!
    echo [OK] Output location: dist\MusicPracticeTracker\
    
    REM Create a zip file for distribution
    echo [INFO] Creating distribution archive...
    cd dist
    powershell -command "Compress-Archive -Path MusicPracticeTracker -DestinationPath MusicPracticeTracker-Windows.zip -Force"
    cd ..
    echo [OK] Distribution archive created: dist\MusicPracticeTracker-Windows.zip
) else (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo ===================================
echo Build Process Complete!
echo ===================================
echo.
echo To run the application:
if "%1"=="--onedir" (
    echo   dist\MusicPracticeTracker\MusicPracticeTracker.exe
) else (
    echo   dist\MusicPracticeTracker.exe
)

pause