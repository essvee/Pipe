#!/bin/sh

echo "Waiting for MySQL..."

while ! mysqladmin ping -h "$DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

echo "MySQL started"

cd /opt/app || exit

mysql --host=$DATABASE_HOST --user=root --password=pass --database=pipe_db --protocol=tcp < deploy/pipe_schema.sql

python -m spacy download en_core_web_md

python -m pipe.src.runme