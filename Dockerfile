# We have to stay on python3.11 - 3.12 has a breaking change in HTTPConnection
FROM python:3.11-alpine

RUN apk -U upgrade --no-cache && \
    apk add git curl

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./testcaldav.py" ]
