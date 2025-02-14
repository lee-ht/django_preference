FROM python:3.11-slim
WORKDIR /app

RUN apt update
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8048
