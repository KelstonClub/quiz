#!/bin/env bash

python -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt &>/dev/null
if [ ! -f quizzes.db ]; then
	python load_into_database.py data.csv
fi
python -mquiz
