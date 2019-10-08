#!/bin/sh

echo "Waiting for MySQL..."

while ! mysqladmin ping -h "$DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

echo "MySQL started"

cd /opt/app || exit

mysql --host=$DATABASE_HOST --user=root --password=pass --database=pipe_db --protocol=tcp < deploy/pipe_schema.sql

wget -O /usr/local/lib/python3.7/site-packages/epitator/importers/doid_extension.ttl https://github.com/ecohealthalliance/EpiTator/raw/master/epitator/importers/doid_extension.ttl
python -m epitator.importers.import_all

python -m pipe.src.runme