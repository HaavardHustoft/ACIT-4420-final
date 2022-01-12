FROM python:3.10.1-alpine

WORKDIR /

COPY requirements.txt .

RUN 'pip install -r -s requirements.txt'


COPY *.py .

CMD ["python", "test.py"]