FROM python:3.10.1-alpine

RUN 'apt-get install -y python-pip'

COPY requirements.txt .

RUN 'pip --version'

COPY *.py .

CMD ["python", "test.py"]