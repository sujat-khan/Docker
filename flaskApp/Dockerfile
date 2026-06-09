# Base image
FROM python:3.11-slim

#work dir
WORKDIR /app

COPY . /app/

#4 Run
RUN pip install --no-cache-dir -r requirements.txt


# Port
EXPOSE 5000

#command
CMD [ "python", "./app.py" ]
