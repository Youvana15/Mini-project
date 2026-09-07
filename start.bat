@echo off
title AI Cyber Deception SOC Dashboard Launcher
cd /d "%~dp0"

echo ======================================================================
echo Starting AI Cyber Deception Decision Framework...
echo ======================================================================
echo.

:: Check python or py
set PYTHON_CMD=
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Using Python launcher: %PYTHON_CMD%
echo.

echo [2/3] Installing/verifying required libraries...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Failed to install some dependencies. Attempting to start anyway...
)
echo.

echo [3/3] Launching application...
echo The dashboard will open in your browser at http://127.0.0.1:8000
echo.
%PYTHON_CMD% run.py

echo.
pause
