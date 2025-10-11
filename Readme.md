 🛡️ Password Checker Project

A DevSecOps-integrated desktop security application built using Python. The project automates password strength analysis, authentication validation, and security assurance through CI/CD pipelines on GitHub. It demonstrates secure software engineering practices by integrating tools like Bandit  ,   pip-audit, Flake8, and Pytest.

---

 🚀 Features
- Password Strength Checker with entropy calculation and feedback.
- Secure Authentication System using bcrypt hashing.
- Brute Force Detection Logs (`bruteforce_local.log`).
- Static Code Analysis using Bandit and Flake8.
- Dependency Vulnerability Scanning using pip-audit.
- Automated Testing with Pytest for functional and security validation.
- GitHub Actions CI/CD Integration for continuous testing and compliance.
- Offline operation – all data stored locally in `users.json`.

---

 📂 Project Structure
```
password-checker-project/
│
├── auth_system.py
├── password_strength_checker.py
├── pytest_security.py
├── bandit_test.py
├── bruteforce_test.py
├── performance_test.py
├── users.json
│
├── requirements.txt
├── setup_run_project.bat
├── create_password_checker_structure.bat
│
├── bandit_report.html / .txt
├── dependency_audit.txt
├── flake8_report.txt
├── pytest_report.txt
│
└── .github/workflows/ci.yml
```

---

 🧩 System Requirements
- Python 3.10 or higher
- pip installed
- Works on Windows, macOS, and Linux

---

 ⚙️ Installation Instructions

 1️⃣ Clone the Repository
```bash
git clone https://github.com/Evolsun365/password-checker-project.git
cd password-checker-project
```

 2️⃣ Create a Virtual Environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate    On Windows
 OR
source venv/bin/activate   On macOS/Linux
```

 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

 4️⃣ Run the Application
```bash
python password_strength_checker.py

---

 🧪 Security Testing

Run Bandit
```bash
bandit -r . -f html -o bandit_report.html
```
Run pip-audit
```bash
pip-audit > dependency_audit.txt
```
Run Flake8
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```
Run Pytest
```bash
pytest -v --maxfail=1 --disable-warnings
```

---

 🔄 CI/CD Workflow
This project includes GitHub Actions for automated testing at `.github/workflows/ci.yml`.  
It runs Bandit, pip-audit, Flake8, and Pytest automatically on every commit.

---

 🪄 Troubleshooting
| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Permission error | Run terminal as Administrator |
| Workflow fails | Validate `.yml` syntax |
| App not running | Use Python 3.10+ |

---

 👥 Contributors
| Name | Role |
|------|------|
| Biki Maharjan | Security & DevSecOps Engineer |
| Suman Adhikari | Lead Developer & Tester |
| Rohit Sharma | Documentation & Compliance Specialist |
| Amrit Sharma | QA Analyst & Reviewer |

---

 📜 License
MIT License — for educational and non-commercial use.

---

Developed for ICT932 – Security Testing and Assurance (Crown Institute of Higher Education).
