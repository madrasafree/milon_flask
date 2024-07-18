#!/bin/bash

# Run Postgres original entrypoint (required for next steps to work)
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

# Create database schemas and load data from dumps
/load_dumps.sh

# Keep the container running by waiting for the original entrypoint script
wait