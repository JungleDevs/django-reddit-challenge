FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

RUN mkdir -p /usr/src/logs
RUN mkdir -p /usr/src/app/static

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]