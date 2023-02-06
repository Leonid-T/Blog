FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt install -y netcat

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./server ./server

WORKDIR ./server
ENTRYPOINT ["/usr/src/app/server/entrypoint.sh"]