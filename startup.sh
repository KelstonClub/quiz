#!/bin/env bash

python -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python load_into_database.py data.csv
python -mquiz
