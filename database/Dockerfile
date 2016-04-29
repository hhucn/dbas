FROM postgres:9.5

COPY . /fixtures
WORKDIR /fixtures

RUN pg_createcluster 9.5 main --start
RUN chmod +x /fixtures/setup.sh

USER postgres
RUN /fixtures/setup.sh

USER root
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.5/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf