FROM python:3.11
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["/bin/bash","./docker/entrypoint.sh"]

EXPOSE 8048