FROM python:3.10-alpine

WORKDIR /stripe-example

ADD . /stripe-example

RUN apk add build-base

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ARG PUB_KEY

ARG STRIPE_SECRET_KEY

ENV PUB_KEY=${PUB_KEY:-YOUR-PUB-KEY}

ENV STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY:-YOUR-STRIPE_SECRET_KEY}

ARG APP_URL

ENV APP_URL=${APP_URL:-http://localhost:8000}

ARG DJANGO_SECRET

ENV DJANGO_SECRET=${DJANGO_SECRET:-YOUR-DJANGO_SECRET}

CMD ["python3", "stripe_example/manage.py", "runserver", "0.0.0.0:8000"]
