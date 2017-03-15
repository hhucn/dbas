FROM hhucn/dbas-build
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

RUN mkdir /dbas

WORKDIR /dbas

COPY requirements.txt /dbas/
RUN pip install -q -U pip \
    && pip install -q -r requirements.txt

COPY . /code/

RUN python setup.py --quiet develop \
    && bash -c 'google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,discussion,review}/*.js > dbas/static/js/dbas.min.js' \
    && sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed \
    && rm -r .sass-cache

CMD ["pserve", "development.ini", "--reload"]
