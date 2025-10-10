# bruteforce_test.py
"""
Robust local brute-force tester.
- auto-cleans a small wordlist file
- auto-detects auth function/class in auth_system.py
- falls back to entropy-only checks if needed
"""

import time
import logging
import os
import importlib
import importlib.util

# ====== CONFIG ======
USERNAME = "testuser"
WORDLIST_FILE = "small_wordlist.txt"
MAX_ATTEMPTS = 200
DELAY_SECONDS = 0.5
STOP_ON_SUCCESS = True
LOG_FILE = "bruteforce_local.log"
# =====================

# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

def ensure_wordlist_is_clean(path):
    """
    Ensure the wordlist exists and remove stray lines like @" or blank lines.
    If it doesn't exist, create a default small wordlist.
    """
    default_list = [
        "123456","password","12345678","qwerty","abc123","letmein","monkey",
        "dragon","iloveyou","111111","admin","welcome","passw0rd","Password1",
        "admin123","1q2w3e4r","sunshine","princess","football","charlie",
        "donald","lovely","freedom","login","master","hello123","trustno1",
        "whatever","Qwerty!2024","S3cur3#Key2025"
    ]
    if not os.path.exists(path):
        logging.info("Wordlist not found; creating default small_wordlist.txt")
        with open(path, "w", encoding="utf-8") as f:
            for p in default_list:
                f.write(p + "\n")
        return default_list

    # read, clean, rewrite
    cleaned = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            # remove stray powershell markers or quoting artifacts
            if s in ("@", '@"', "@'", "''", '""'):
                continue
            if s == "":
                continue
            cleaned.append(s)
    if not cleaned:
        logging.info("Wordlist was empty after cleaning; writing defaults")
        with open(path, "w", encoding="utf-8") as f:
            for p in default_list:
                f.write(p + "\n")
        return default_list
    # overwrite with cleaned lines
    with open(path, "w", encoding="utf-8") as f:
        for p in cleaned:
            f.write(p + "\n")
    return cleaned

def detect_auth():
    """
    Try to find an authentication function or class in auth_system.py
    Returns a callable authenticate(username, password) or None.
    """
    # Strategy:
    # 1) Try from auth_system import authenticate
    # 2) Try from auth_system import AuthSystem; instantiate and use method
    # 3) Try importing password_strength_checker for a method like auth or login
    # 4) Return None -> fallback to entropy-only simulation

    candidates = [
        ("auth_system", "authenticate", "func"),
        ("auth_system", "AuthSystem", "class"),
        ("password_strength_checker", "authenticate", "func"),
        ("password_strength_checker", "AuthSystem", "class"),
    ]

    for module_name, member, typ in candidates:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                continue
            mod = importlib.import_module(module_name)
            if typ == "func" and hasattr(mod, member):
                func = getattr(mod, member)
                if callable(func):
                    logging.info("Using function %s.%s as authenticate", module_name, member)
                    return lambda u, p: func(u, p)
            if typ == "class" and hasattr(mod, member):
                cls = getattr(mod, member)
                try:
                    # try instantiate with no args, else try common args
                    try:
                        inst = cls()
                    except TypeError:
                        # try with users.json if exists
                        if os.path.exists("users.json"):
                            inst = cls("users.json")
                        else:
                            inst = cls(None)
                    if hasattr(inst, "authenticate") and callable(getattr(inst, "authenticate")):
                        logging.info("Using %s.%s().authenticate as authenticate", module_name, member)
                        return lambda u, p: inst.authenticate(u, p)
                except Exception as e:
                    logging.info("Could not instantiate %s: %s", member, e)
        except Exception as e:
            logging.debug("Import attempt failed: %s - %s", module_name, e)
            continue
    return None

# entropy fallback
import math
def entropy_only_auth(username, password):
    """
    Fallback: treat strength > threshold as 'not accepted' (simulate)
    This does NOT authenticate — used only to demonstrate weak passwords.
    """
    pool = 0
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digits = any(c.isdigit() for c in password)
    symbols = any(not c.isalnum() for c in password)

    if lower: pool += 26
    if upper: pool += 26
    if digits: pool += 10
    if symbols: pool += 32

    ent = len(password) * (math.log2(pool) if pool > 0 else 0)
    # assume success only if entropy extremely low (this is inverted: for demo we treat high entropy as 'safe')
    # For brute-force demo, we say authenticate returns True only if password matches a hidden correct one:
    return False  # always fail – indicates no real auth available

def run():
    logging.info("Starting local brute-force test against user: %s", USERNAME)

    # ensure wordlist
    candidates = ensure_wordlist_is_clean(WORDLIST_FILE)
    logging.info("Using wordlist with %d entries (first 5): %s", len(candidates), candidates[:5])

    # detect auth
    auth_callable = detect_auth()
    if auth_callable is None:
        logging.warning("No auth function detected in project. Falling back to entropy-only simulation (no real auth).")
        auth_callable = entropy_only_auth
        fallback = True
    else:
        fallback = False

    attempts = 0
    for pwd in candidates:
        if attempts >= MAX_ATTEMPTS:
            logging.info("Reached MAX_ATTEMPTS (%d). Stopping.", MAX_ATTEMPTS)
            break
        attempts += 1
        logging.info("Attempt %d: testing password '%s'", attempts, pwd)

        try:
            ok = auth_callable(USERNAME, pwd)
        except Exception as e:
            logging.exception("Error calling authenticate(): %s", e)
            break

        if ok:
            logging.info("SUCCESS: credentials found -> %s : %s", USERNAME, pwd)
            if STOP_ON_SUCCESS:
                break
        else:
            if fallback:
                # if fallback we can log entropy to show weak/strong for reporting
                pool = 0
                lower = any(c.islower() for c in pwd)
                upper = any(c.isupper() for c in pwd)
                digits = any(c.isdigit() for c in pwd)
                symbols = any(not c.isalnum() for c in pwd)
                if lower: pool += 26
                if upper: pool += 26
                if digits: pool += 10
                if symbols: pool += 32
                ent = len(pwd) * (math.log2(pool) if pool > 0 else 0)
                logging.info("Simulated check (no auth): Password: %s | Entropy: %.2f", pwd, ent)
            else:
                logging.info("Failed")

        time.sleep(DELAY_SECONDS)

    logging.info("Brute-force test completed. Total attempts: %d", attempts)

if __name__ == "__main__":
    run()
