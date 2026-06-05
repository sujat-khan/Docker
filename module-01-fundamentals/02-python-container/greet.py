"""greet.py — demonstrates reading environment variables from -e flags."""
import os

name = os.getenv("STUDENT_NAME", "World")
course = os.getenv("COURSE", "Docker Fundamentals")

print(f"\n👋 Hello, {name}!")
print(f"   Welcome to: {course}")
print(f"   You're running Python inside Docker.")
print(f"   Environment variables were injected with -e flags.\n")
