# NextEws
Simple flask website that make text classification using neural networks on news

## Set up
To set up the your flask application follow these steps:
* Create a virtual environment `python3 -m venv nextews_env`
* Install flask `pip install flask`
* Install the follow libraries:
    * `pandas`
* Set the virtual environment `source nextews_env/bin/activate`
* Set the flask information:
    * `export FLASK_APP=nextews`
    * `export FLASK_ENV=development`
    * `export FLASK_DEBUG=true`
* Initialize the database `flask init-db`
* Now you can start your flask app `flask run`

In case it gaves you encoding problems set `export LC_ALL=en_us.UTF-8` and `export LANG=en_us.UTF-8`