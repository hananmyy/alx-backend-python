FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 8000
# For reference: -p 8000:8000 is used at runtime
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
