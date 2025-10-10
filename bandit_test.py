#!/usr/bin/env python3
"""
Bandit security test example for our password checker
Run with: bandit -r password_strength_checker.py
"""

import subprocess
import sys

def run_bandit():
    """Run Bandit SAST tool on our code"""
    try:
        result = subprocess.run([
            'bandit', '-r', 'password_strength_checker.py', 'auth_system.py',
            '-f', 'html', '-o', 'bandit_report.html'
        ], capture_output=True, text=True)
        
        print("Bandit SAST Results:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except FileNotFoundError:
        print("Bandit not installed. Install with: pip install bandit")
        return False

if __name__ == "__main__":
    run_bandit()