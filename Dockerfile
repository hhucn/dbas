FROM python:3.5

MAINTAINER Christian Meter <meter@cs.uni-duesseldorf.de>

RUN mkdir /code
WORKDIR /code

ADD . /code/

ADD requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt

# RUN apt-get update
# RUN apt-get --yes install sudo

RUN python setup.py develop

# RUN initialize_discussion_sql development.ini
# RUN initialize_news_sql development.ini

# RUN pserve development.ini --reload