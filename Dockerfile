FROM python:3.5
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt

ADD . /code/

RUN python setup.py develop
