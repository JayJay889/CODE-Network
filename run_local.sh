#!/bin/bash
# Run the Flask app locally with a MongoDB instance
cd "$(dirname "$0")"
source venv/bin/activate

# Default to a local MongoDB if MONGO_URI is not already set
export MONGO_URI="${MONGO_URI:-mongodb://127.0.0.1:27017/contacts_db}"

python3 app.py

