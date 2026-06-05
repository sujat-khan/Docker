"""
app.py — The Python script our Docker image will run.

This uses only the Python standard library (no pip install needed).
We'll add dependencies in the next lesson.
"""
import os
import sys
import platform
from datetime import datetime

YOUR_NAME = os.getenv("YOUR_NAME", "World")

print()
print("=" * 55)
print("   🐳  My First Docker Image is Working!")
print("=" * 55)
print(f"   Hello, {YOUR_NAME}!")
print(f"   Python version  : {sys.version.split()[0]}")
print(f"   OS inside Docker: {platform.system()} {platform.release()}")
print(f"   Machine arch    : {platform.machine()}")
print(f"   Working dir     : {os.getcwd()}")
print(f"   Timestamp       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 55)
print()
print("   This script is running INSIDE a Docker container.")
print("   The container was built from our Dockerfile.")
print("   The image contains Python 3.11-slim + this script.")
print()
