FROM python:3.10.1-alpine

COPY requirements.txt .

RUN 'pip install -r requirements.txt'

COPY *.py .

CMD ["python", "test.py"]