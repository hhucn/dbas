FROM python:3.5
MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

# Add sources for nodejs
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -

RUN apt-get update -qq && \
    apt-get install -yqq rubygems nodejs && \
    (yes | gem install sass) && \
    npm install bower phantomjs-prebuilt -g && \
    mkdir /code

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -U pip && \
    pip install -r requirements.txt

ADD . /code/

RUN python setup.py develop
