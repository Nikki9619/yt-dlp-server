FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY server.py .

CMD ["python", "server.py"]
