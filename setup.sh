#!/bin/bash

read -r -d '' intro << EOM
================================================================
NextEws
================================================================
Inizializzazione del progetto ...
EOM

echo "$intro"
# Download data
curl -L 'https://www.dropbox.com/s/bjveo6hspxluqud/nextews.zip?dl=0' > nextews/static/util.zip
unzip nextews/static/util.zip -d nextews/static/ && rm nextews/static/util.zip

python3 -m venv .env
source .env/bin/activate
python3 -m pip install -r requirements.txt
deactivate

python -m nltk.downloader all
flask init-db
