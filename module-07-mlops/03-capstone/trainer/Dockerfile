FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir mlflow scikit-learn numpy boto3 psycopg2-binary
COPY . .
