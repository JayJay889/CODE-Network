#!/bin/bash
cd "$(dirname "$0")"
# Render automatically handles python environment, no need to activate venv manually if it fails
# or we can try to activate the one Render creates if we really want to, but python app.py usually works if dependencies are installed
python3 app.py
