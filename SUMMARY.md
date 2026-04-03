# Project Summary

This project serves a pre-trained banana leaf disease classifier via a Flask API. No training runs on deploy.

## Key Points

- Pre-trained model in models/banana_model.h5
- Metadata in models/metadata.json
- Render deployment with gunicorn
- Optional external fallback via BACKUP_SVC

## Deploy (Render)

Build Command:

pip install -r requirements.txt

Start Command:

gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app

## API

- GET /health
- GET /info
- POST /predict
