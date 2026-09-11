#!/bin/sh

echo "migrations running ..."
alembic upgrade head

echo "starting fastapi services ..."
# gunicorn --reload app.main:app --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker --workers 4 
uvicorn --reload app.main:app --host 0.0.0.0 --port 8000 