FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install Jupyter and ML packages
RUN pip install --no-cache-dir \
    jupyterlab==4.0.9 \
    numpy==1.26.2 \
    pandas==2.1.4 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2

# Create notebooks directory
RUN mkdir -p /app/notebooks

EXPOSE 8888

# Start Jupyter Lab
# --no-browser        = don't try to open a browser (no GUI in Docker)
# --ip=0.0.0.0        = listen on all interfaces (required for Docker)
# --allow-root        = we're running as root in the container
# --NotebookApp.token = empty string = no auth (for local dev only!)
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--notebook-dir=/app/notebooks", \
     "--ServerApp.token=''"]
