FROM python:alpine
RUN set -ex && mkdir /app
WORKDIR /app
# uncomment if using uwsgi
# RUN apk add python3-dev build-base linux-headers pcre-dev
COPY . .

RUN pip3 install pipenv && pipenv install --deploy --system

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:80
