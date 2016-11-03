FROM hhucn/dbas-build
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -U pip && \
    pip install -r requirements.txt

ADD . /code/

RUN python setup.py develop
