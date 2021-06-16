FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV UWSGI_INI /app/uwsgi.ini

COPY ./app /app

COPY requirements.txt .
RUN pip install -r requirements.txt

