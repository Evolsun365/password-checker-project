<<<<<<< HEAD
@echo off
REM ============================================
REM DevSecOps Automated Testing Pipeline (Fixed)
REM ============================================

cd /d "C:\Users\evo_m\Desktop\Security testing\password-checker-project"

REM Create reports folder if missing
if not exist "reports" mkdir reports

echo.
echo [1/4] Running Bandit (Static Application Security)...
python -m bandit -r . -f txt -o "reports\bandit_report.txt"
echo Bandit scan complete. Report saved to reports\bandit_report.txt
echo.

echo [2/4] Running pip-audit (Dependency Vulnerability Scan)...
python -m pip_audit > "reports\dependency_audit.txt"
echo pip-audit complete. Report saved to reports\dependency_audit.txt
echo.

echo [3/4] Running Flake8 (Code Quality Check)...
python -m flake8 . --statistics --exclude=venv,__pycache__,.git,*.pyc > "reports\flake8_report.txt"
echo Flake8 analysis complete. Report saved to reports\flake8_report.txt
echo.

echo [4/4] Running Pytest (Functional & Security Tests)...
python -m pytest pytest_security.py -v > "reports\pytest_report.txt"
echo Pytest complete. Report saved to reports\pytest_report.txt
echo.

echo ============================================
echo All tests finished successfully!
echo Reports available at:
echo %cd%\reports
echo ============================================

pause
=======
@echo off
REM ============================================
REM DevSecOps Automated Testing Pipeline (Fixed)
REM ============================================

cd /d "C:\Users\evo_m\Desktop\Security testing\password-checker-project"

REM Create reports folder if missing
if not exist "reports" mkdir reports

echo.
echo [1/4] Running Bandit (Static Application Security)...
python -m bandit -r . -f txt -o "reports\bandit_report.txt"
echo Bandit scan complete. Report saved to reports\bandit_report.txt
echo.

echo [2/4] Running pip-audit (Dependency Vulnerability Scan)...
python -m pip_audit > "reports\dependency_audit.txt"
echo pip-audit complete. Report saved to reports\dependency_audit.txt
echo.

echo [3/4] Running Flake8 (Code Quality Check)...
python -m flake8 . --statistics --exclude=venv,__pycache__,.git,*.pyc > "reports\flake8_report.txt"
echo Flake8 analysis complete. Report saved to reports\flake8_report.txt
echo.

echo [4/4] Running Pytest (Functional & Security Tests)...
python -m pytest pytest_security.py -v > "reports\pytest_report.txt"
echo Pytest complete. Report saved to reports\pytest_report.txt
echo.

echo ============================================
echo All tests finished successfully!
echo Reports available at:
echo %cd%\reports
echo ============================================

pause
>>>>>>> c1bae8b7eae4dc0ad8876edf87befbb6e1b0111f
