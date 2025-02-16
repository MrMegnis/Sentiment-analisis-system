FROM python:3.11-slim

WORKDIR ./sent-analisis-app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

COPY datasets/ ./datasets

EXPOSE 5000

CMD ["sh", "-c", "ls -la && python app/app.py"]
