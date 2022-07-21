nohup gunicorn bulletin_board.wsgi:application --bind 0.0.0.0:8000 &
daphne bulletin_board.asgi:application -b 0.0.0.0 -p 8001