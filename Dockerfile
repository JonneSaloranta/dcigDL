FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

RUN apk update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
