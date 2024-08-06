#!/bin/bash

# Run Postgres original entrypoint (required for next steps to work)
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

schema_exists=$(psql -h localhost -p 5432 -U postgres -Atc \
"SELECT 1 FROM information_schema.schemata WHERE schema_name = 'public';")

# Trim whitespace
schema_exists=$(echo $schema_exists | xargs)

if [ "$schema_exists" = "1" ]; then
    echo "Schema exists. Skipping schema loading."
else
    echo "Schema does not exist. Loading dumps..."
    /load_dumps.sh
fi

# Keep the container running by waiting for the original entrypoint script
wait