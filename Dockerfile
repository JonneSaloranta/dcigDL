FROM python:3.10-alpine

WORKDIR /app

RUN apk update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]