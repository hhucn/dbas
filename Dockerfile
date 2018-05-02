FROM python:3.6.4-slim-stretch as python-base
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

ENV locs /etc/locale.gen

RUN apt-get update -qq && \
    apt-get install -yqq build-essential libfontconfig locales libsasl2-dev libldap2-dev libssl-dev gettext bzip2 autoconf libffi-dev gcc iproute2

RUN touch $locs && \
    echo "de_DE.UTF-8 UTF-8" >> $locs && \
    echo "en_US.UTF-8 UTF-8" >> $locs && \
    locale-gen && \
    echo "Europe/Berlin" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt .

RUN python3 -m pip install --upgrade  -r requirements.txt
COPY . /dbas/


FROM python:3.6-alpine3.7

COPY --from=python-base /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY --from=python-base /root/.cache/ /root/.cache/

COPY --from=python-base /etc/timezone /etc/timezone
COPY --from=python-base /dbas/ /dbas/

WORKDIR /dbas/

RUN apk update && \
    apk add --no-cache yarn gettext libldap nodejs bash musl-dev postgresql-dev&& \
    npm install -g sass google-closure-compiler-js

RUN apk update && \
    apk add --virtual .build-deps gcc &&\
    python3 -m pip install --upgrade --no-deps --force-reinstall  -r requirements.txt &&\
    ./build_assets.sh &&\
    rm -r /root/.cache &&\
    apk del .build-deps

EXPOSE 4284
CMD sh -c "alembic upgrade head && pserve development.ini --reload"
