"""
hello.py — Lesson 2: Running Python Scripts in Docker

This script uses only the Python standard library.
No pip install needed — the official python:3.11-slim image includes it all.
"""
import sys
import os
import platform
from datetime import datetime

print("=" * 50)
print("  🐳 Hello from inside a Docker container!")
print("=" * 50)
print(f"  Python version : {sys.version.split()[0]}")
print(f"  Platform       : {platform.system()} {platform.release()}")
print(f"  Working dir    : {os.getcwd()}")
print(f"  Time           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  User name      : {os.getenv('STUDENT_NAME', 'World')}")
print("=" * 50)
