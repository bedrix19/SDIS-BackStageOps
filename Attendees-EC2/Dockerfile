FROM python:latest

WORKDIR /try

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD test.py

CMD ["python", "./test.py"]