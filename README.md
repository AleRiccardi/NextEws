# NextEws
Simple flask website that make text classification using neural networks on news

## Set up
To set up the your flask application follow these steps:
* Create a virtual environment `python3 -m venv myvenv`
* Install flask `pip install flask`
* Install the follow libraries:
    * `pandas`
* Set the flask information:
    * `export FLASK_APP=nextews`
    * `export FLASK_ENV=development`
* Initialize the database `flask init-db`
* Now you can start your flask app `flask run`