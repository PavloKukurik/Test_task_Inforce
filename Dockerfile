FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN chmod +x /app/start.sh

CMD ["./start.sh"]
