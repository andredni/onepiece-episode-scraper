FROM python:slim-bookworm

COPY requirements.txt /app/requirements.txt
COPY index.py /app/index.py

RUN pip install -r /app/requirements.txt

CMD python /app/index.py