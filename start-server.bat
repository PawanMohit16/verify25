@echo off
REM Quick start script for local server
REM Usage: double-click this file to start the server

cd /d "%~dp0"
echo.
echo Starting local server for verify25...
echo.
python server.py
pause
