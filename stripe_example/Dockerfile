FROM python:3.10

WORKDIR /stripe-example

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

RUN apt-get update \
  && apt-get install netcat gcc \
  && apt-get clean

COPY . .

CMD ["sh", "run_uwsgi.sh"]