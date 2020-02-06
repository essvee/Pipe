#!/bin/sh

echo "Waiting for MySQL..."

while ! mysqladmin ping -h "$DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

echo "MySQL started"

cd /opt/app || exit

mysql --host=$DATABASE_HOST --user=root --password=pass --database=annette_db --protocol=tcp < deploy/annette_schema.sql

if [ ! -f "/root/.epitator.sqlitedb" ]; then
  # this doesn't work if you put it in the Dockerfile but
  # it takes ages so we only want to do it once
  echo "Importing epitator"
  python -m epitator.importers.import_all
fi

if [ -f "annette/data/gmail-credentials.json" ]; then
  python -m annette.src.runme
else
  echo "Now run:\n\tdocker run -it annette_backend python /opt/app/deploy/auth.py --noauth_local_webserver"
fi
