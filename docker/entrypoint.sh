#!/bin/bash

python manage.py migrate
python manage.py collectstatic
daphne config.asgi:application -b 0.0.0.0 -p 8048