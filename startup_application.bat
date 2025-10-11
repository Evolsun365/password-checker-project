@echo off
REM Portable runner for auth_system.py
REM Place this file in the same folder as auth_system.py

REM Get folder where this .bat is located (handles spaces)
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash for cosmetic reasons (optional)
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

cd /d "%SCRIPT_DIR%"

echo Running from: "%SCRIPT_DIR%"
echo.

REM If a venv exists inside the project, use it
if exist "%SCRIPT_DIR%\venv\Scripts\activate.bat" (
    echo Activating venv...
    call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
    echo Running auth_system.py with venv python...
    python auth_system.py %*
    REM optional: deactivate (Windows venv deactivate is a function in the shell)
    call deactivate 2>nul
    goto PAUSE
)

REM Try using the py launcher (recommended if installed)
where py >nul 2>nul
if %errorlevel%==0 (
    echo Found py launcher. Running with "py -3".
    py -3 auth_system.py %*
    goto PAUSE
)

REM Try python on PATH
where python >nul 2>nul
if %errorlevel%==0 (
    echo Found python on PATH. Running with "python".
    python auth_system.py %*
    goto PAUSE
)

echo ERROR: No Python found.
echo - Install Python 3 from https://www.python.org/ and check "Add Python to PATH"
echo - OR create a virtual environment in this folder (python -m venv venv) and re-run this .bat
echo.
echo To create and use a venv (one-time):
echo    1) Open CMD in this folder
echo    2) python -m venv venv
echo    3) venv\Scripts\activate.bat
echo    4) pip install -r requirements.txt
echo    5) run this run_auth.bat
echo.

:PAUSE
echo.
echo Press any key to close...
pause >nul
