@echo off
set FLASK_APP=app.py
set FLASK_ENV=production
set PYTHONPATH=%cd%
venv\Scripts\gunicorn app:app --bind=127.0.0.1:5000 --workers=4 --access-logfile=-