<<<<<<< HEAD
# pytest_security.py
import os
import tkinter as tk
from password_strength_checker import ModernPasswordChecker

def test_password_entropy():
    """Verify entropy calculation for a strong password"""
    root = tk.Tk()  # create dummy root window
    root.withdraw()  # hide the window (prevents GUI popup)
    checker = ModernPasswordChecker(root, "User", "TestUser")  # pass valid root
    password = "StrongPass123!"
    entropy = checker.calculate_entropy(password)
    assert entropy > 60, f"Entropy too low: {entropy}"
    root.destroy()  # clean up after test

def test_audit_log_exists():
    """Check that the audit log file is generated"""
    assert os.path.exists("app_audit.log"), "Audit log file missing"
=======
# pytest_security.py
import os
import tkinter as tk
from password_strength_checker import ModernPasswordChecker

def test_password_entropy():
    """Verify entropy calculation for a strong password"""
    root = tk.Tk()  # create dummy root window
    root.withdraw()  # hide the window (prevents GUI popup)
    checker = ModernPasswordChecker(root, "User", "TestUser")  # pass valid root
    password = "StrongPass123!"
    entropy = checker.calculate_entropy(password)
    assert entropy > 60, f"Entropy too low: {entropy}"
    root.destroy()  # clean up after test

def test_audit_log_exists():
    """Check that the audit log file is generated"""
    assert os.path.exists("app_audit.log"), "Audit log file missing"
>>>>>>> c1bae8b7eae4dc0ad8876edf87befbb6e1b0111f
