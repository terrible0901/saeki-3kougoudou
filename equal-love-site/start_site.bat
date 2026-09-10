@echo off
setlocal
cd /d "%~dp0"
title EQUAL LOVE FAN REVIEW

if exist ".venv\Scripts\python.exe" goto verify_dependencies

set "PYTHON="
py -c "import sys" >nul 2>&1 && set "PYTHON=py"
if not defined PYTHON python -c "import sys" >nul 2>&1 && set "PYTHON=python"
if not defined PYTHON goto no_python

"%PYTHON%" -m venv .venv
if errorlevel 1 goto setup_error

:verify_dependencies
".venv\Scripts\python.exe" -c "import flask" >nul 2>&1
if errorlevel 1 (
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto setup_error
)

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"
".venv\Scripts\python.exe" app.py
if errorlevel 1 goto run_error
goto end

:no_python
echo Python 3 is required. Install Python, then run this file again.
pause
goto end

:setup_error
echo Setup failed. Check your internet connection and try again.
pause
goto end

:run_error
echo The site stopped because of an error. Check the message above.
pause

:end
endlocal
