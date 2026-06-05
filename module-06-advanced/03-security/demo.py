"""
demo.py — Security lesson demo script.
Shows who is running the process and what filesystem access is available.
"""
import os
import sys

print("=" * 50)
print("  🔒 Docker Security Demo")
print("=" * 50)
print(f"  Running as user : {os.getenv('USER', 'unknown')} (UID={os.getuid() if hasattr(os, 'getuid') else 'N/A'})")
print(f"  Python          : {sys.version.split()[0]}")
print(f"  Working dir     : {os.getcwd()}")

# Try writing to a sensitive location
try:
    with open("/etc/test_write", "w") as f:
        f.write("hacked!")
    print("  /etc write      : ✅ ALLOWED (dangerous!)")
except PermissionError:
    print("  /etc write      : 🔒 BLOCKED (good!)")

# Try reading /etc/passwd
try:
    with open("/etc/passwd") as f:
        first_line = f.readline().strip()
    print(f"  /etc/passwd     : readable (first line: {first_line[:40]}...)")
except Exception as e:
    print(f"  /etc/passwd     : {e}")

print("=" * 50)
