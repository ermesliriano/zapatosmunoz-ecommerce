FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY init_db.py init_db.py
COPY inventory.db inventory.db
COPY shared /app/shared

CMD ["python", "app.py"]
