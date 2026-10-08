@echo off
cd /d "C:\Users\VERONICA\OneDrive\Desktop\PROYECTOS\etl-ventas-sqlserver-powerbi"
venv\Scripts\python.exe scripts\etl_main.py
exit /b %ERRORLEVEL%