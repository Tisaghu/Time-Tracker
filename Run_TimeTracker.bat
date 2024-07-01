@echo off
REM Get the directory of the batch file
set "BASEDIR=%~dp0"
cd /d "%BASEDIR%"

REM Run the Python script to start the Flask app
echo Starting Flask app...
start /B python TimeTracker.py

REM Wait a few seconds for the server to start
timeout /t 2 /nobreak >nul

REM Open the default web browser to URL
start "" "http://127.0.0.1:5000"

pause
