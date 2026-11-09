@echo off
cd /d "%~dp0"
python genesis_ui.py
if errorlevel 1 pause
