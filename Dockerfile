FROM python:3.10.1-alpine

COPY requirements.txt .

RUN 'pip --version'

COPY *.py .

CMD ["python", "test.py"]