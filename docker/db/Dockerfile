FROM postgres:10-alpine
ENV TZ Europe/Berlin
COPY ./entrypoint/* /docker-entrypoint-initdb.d/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone