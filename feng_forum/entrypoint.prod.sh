#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

rm feng_forum/urls.py
cp feng_forum/fakeurls.py feng_forum/urls.py
# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic -c --no-input > trash
rm feng_forum/urls.py
cp feng_forum/realurls.py feng_forum/urls.py
# python manage.py shell < delete_content_type.py
# python manage.py loaddata db.json
exec "$@"