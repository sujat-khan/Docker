"""
data_info.py — shows system/environment info from inside the container.
Standard library only — no pip required.
"""
import os
import sys
import platform
import socket

print("\n📦 Container Environment Info")
print("-" * 40)
print(f"Hostname (container ID): {socket.gethostname()}")
print(f"OS:                      {platform.system()}")
print(f"OS release:              {platform.release()}")
print(f"Architecture:            {platform.machine()}")
print(f"Python:                  {sys.version}")
print(f"Working directory:       {os.getcwd()}")
print(f"Files visible here:      {os.listdir('.')}")
print("-" * 40)

# Show environment variables (Docker injects some)
print("\n🔧 Environment Variables:")
docker_vars = {k: v for k, v in os.environ.items()
               if any(k.startswith(p) for p in ('PATH', 'PYTHON', 'HOME', 'STUDENT', 'COURSE'))}
for k, v in docker_vars.items():
    print(f"  {k} = {v}")
