FROM python:3.6-slim
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

ENV locs /etc/locale.gen

RUN apt-get update -qq && \
    apt-get install -yqq curl && \
    curl -sL https://deb.nodesource.com/setup_7.x | bash - && \
    apt-get install -yqq ruby2.1-dev rubygems build-essential nodejs locales libsasl2-dev python-dev libldap2-dev libssl-dev gettext bzip2 && \
    (yes | gem install sass) && \
    npm install bower phantomjs-prebuilt google-closure-compiler-js -g && \
    touch $locs && \
    echo "de_DE.UTF-8 UTF-8" >> $locs && \
    echo "en_US.UTF-8 UTF-8" >> $locs && \
    locale-gen && \
    echo 'Europe/Berlin' > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get remove -y --purge curl bzip2 && \
    apt-get autoremove -y && \
    apt-get clean && \
    npm cache clean && \
    gem cleanup && \
    mkdir /dbas

WORKDIR /dbas

COPY requirements.txt /dbas/

RUN apt-get install -y build-essential libfontconfig && \
    pip install -q -U pip && \
    pip install -q -r requirements.txt && \
    apt-get remove -y --purge build-essential && \
    apt-get autoremove -y && \
    apt-get clean -y

COPY . /dbas/

RUN python setup.py --quiet develop \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,d3,discussion,review}/*.js > dbas/static/js/dbas.min.js' \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/libs/cookie-2.1.3.js > dbas/static/js/libs/cookie-2.1.3.min.js' \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/libs/eu-cookie-law-popup.js > dbas/static/js/libs/eu-cookie-law-popup.min.js' \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./webhook/static/js/*.js > webhook/static/js/websocket.min.js' \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./admin/static/js/main/*.js > admin/static/js/admin.min.js' \
    && sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed \
    && sass dbas/static/css/creative.sass dbas/static/css/creative.css --style compressed \
    && rm -r .sass-cache \
    && cd dbas && ./i18n.sh \
    && cd ../admin && ./i18n.sh \
    && cd ../

EXPOSE 4284
CMD ["pserve", "development.ini", "--reload"]
