#!/bin/bash

psql -h localhost -p 5432 -U postgres -d arabicWords -f ./db_dumps/arabicWords_schema.sql
psql -h localhost -p 5432 -U postgres -d arabicWords -f ./db_dumps/arabicWords_data.sql
psql -h localhost -p 5432 -U postgres -d arabicUsers -f ./db_dumps/arabicUsers_schema.sql
psql -h localhost -p 5432 -U postgres -d arabicUsers -f ./db_dumps/arabicUsers_data.sql
echo "dump load done"