FROM python:3.7-slim

ENV locs /etc/locale.gen
ENV TEMPLATE_FOLDER /dbas/dbas/templates/
ENV CHAMELEON_CACHE ${TEMPLATE_FOLDER}cache

RUN apt-get update -qq && \
    apt-get install -yqq curl gnupg2 make && \
    curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update -qq && \
    apt-get install -yqq build-essential libpq-dev python-dev libfontconfig nodejs locales libsasl2-dev libldap2-dev libssl-dev gettext bzip2 autoconf libffi-dev gcc iproute2 yarn && \
    npm install npx google-closure-compiler sass -g && \
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
    mkdir /dbas

WORKDIR /dbas

COPY requirements.txt /dbas/

RUN pip install -q -U pip && \
    pip install -r requirements.txt && \
    apt-get remove -y --purge build-essential gcc&& \
    apt-get autoremove -y && \
    apt-get clean -y

COPY . /dbas/

RUN make && python3 precompile_templates.py --dir ${TEMPLATE_FOLDER}

EXPOSE 4284
CMD sh -c "alembic upgrade head && pserve development.ini --reload"
