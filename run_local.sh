#!/bin/bash
# Run the Flask app locally with SQLite database
cd "$(dirname "$0")"
source venv/bin/activate
export USE_SQLITE=true
python3 app.py

