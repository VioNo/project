FROM python:3.10-slim

#системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./app/install.txt .
RUN pip install --no-cache-dir -r install.txt

COPY ./app .

#запускаем через run.py, который в корне
CMD ["python", "run.py"]