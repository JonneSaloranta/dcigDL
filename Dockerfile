FROM python:3.10-alpine as builder

WORKDIR /app

RUN apk update && \
    apk add --no-cache git && \
    git clone https://github.com/JonneSaloranta/dcigDL.git . && \
    pip install -r requirements.txt

FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /app /app

CMD ["python", "main.py"]
