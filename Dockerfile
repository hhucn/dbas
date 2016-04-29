FROM python:3.5

MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get --yes install sudo

ADD . /code/
# RUN make init
# RUN make all
RUN python setup.py develop

