FROM postgres:9.5

RUN pg_createcluster 9.5 main --start

USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER dbas WITH SUPERUSER PASSWORD 'gAjOVf8MHBgHwUH8NmyWqwQQ43En1b0Mk1wZbm2JOYzWJ8PrQbwEIoWRhz4zT6Wz';" &&\
    createdb -O dbas discussion &&\
    createdb -O dbas news

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

#EXPOSE 5432

CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]


# USER root
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.

# And add ``listen_addresses`` to ``/etc/postgresql/9.5/main/postgresql.conf``
