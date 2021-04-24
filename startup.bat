py -mvenv .venv
CALL .venv\Scripts\activate
pip install -r requirements.txt
py load_into_database.py data.csv
py -mquiz
