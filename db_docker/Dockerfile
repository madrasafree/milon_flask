FROM postgres:16.3

COPY ./db_dumps /db_dumps
COPY 01-create_dbs.sql /docker-entrypoint-initdb.d/
COPY load_dumps.sh /
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /load_dumps.sh /docker-entrypoint.sh

ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_DB postgres

ENTRYPOINT ["/docker-entrypoint.sh"]