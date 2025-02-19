FROM python:3.11-slim

WORKDIR /contest

COPY requirements.txt /contest/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /contest/model/ /contest/model/
COPY /contest/solution.py /contest/solution.py
COPY /contest/data.csv /contest/data.csv

ENV TRANSFORMERS_OFFLINE=1

CMD ["python", "/contest/solution.py"]
