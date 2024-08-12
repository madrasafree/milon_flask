FROM postgres:16.3

COPY ./db_dumps /db_dumps
COPY 01-create_dbs.sql /docker-entrypoint-initdb.d/
COPY load_dumps.sh /
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN apt-get update && apt-get install -y dos2unix

RUN dos2unix /docker-entrypoint.sh /load_dumps.sh

RUN chmod +x /load_dumps.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]