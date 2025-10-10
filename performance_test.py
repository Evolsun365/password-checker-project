# performance_test.py
import time
import math

# lightweight entropy function (same logic as our brute-force test)
def calculate_entropy(password):
    pool = 0
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digits = any(c.isdigit() for c in password)
    symbols = any(not c.isalnum() for c in password)

    if lower: pool += 26
    if upper: pool += 26
    if digits: pool += 10
    if symbols: pool += 32

    # avoid math domain error if pool == 0
    entropy = len(password) * (math.log2(pool) if pool > 0 else 0)
    return round(entropy, 2)

# Generate N test passwords (mix of complexity)
def make_password(i):
    # simple deterministic mix: vary length, include digits/symbols based on i
    base = f"Pass{i}"
    if i % 3 == 0:
        return base + "123!"
    if i % 5 == 0:
        return base + "Aa1#Bb2$"
    return base + "abcd"

def run_performance_test(num_passwords=1000):
    start = time.time()
    for i in range(num_passwords):
        p = make_password(i)
        _ = calculate_entropy(p)
    end = time.time()
    elapsed = end - start
    per_item = elapsed / num_passwords if num_passwords else 0
    print(f"Processed {num_passwords} passwords in {elapsed:.2f} seconds "
          f"({per_item:.4f} sec/password)")

if __name__ == "__main__":
    # change the number below if you want a lighter/heavier test
    run_performance_test(num_passwords=500)
