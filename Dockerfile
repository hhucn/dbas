FROM python:3.6.4-slim-stretch
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

ENV locs /etc/locale.gen

RUN apt-get update -qq && \
    apt-get install -yqq curl gnupg2 && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -yqq ruby2.3-dev rubygems build-essential libfontconfig nodejs locales libsasl2-dev libldap2-dev libssl-dev gettext bzip2 autoconf libffi-dev gcc && \
    (yes | gem install sass) && \
    npm install phantomjs-prebuilt -g && \
    npm install google-closure-compiler-js -g && \
    touch $locs && \
    echo "de_DE.UTF-8 UTF-8" >> $locs && \
    echo "en_US.UTF-8 UTF-8" >> $locs && \
    locale-gen && \
    echo "Europe/Berlin" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get remove -y --purge curl bzip2 && \
    apt-get autoremove -y && \
    apt-get clean && \
    npm cache clean --force && \
    gem cleanup && \
    mkdir /dbas

WORKDIR /dbas

COPY requirements.txt /dbas/

RUN pip install -q -U pip && \
    pip install -r requirements.txt && \
    apt-get remove -y --purge build-essential gcc&& \
    apt-get autoremove -y && \
    apt-get clean -y

COPY . /dbas/

RUN ./build_assets.sh

EXPOSE 4284
CMD ["pserve", "development.ini", "--reload"]
