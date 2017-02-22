'''Main file to register blueprints and run the flask application'''
import configparser
from flask import Flask
from chefboyrd import views
from chefboyrd.views import index

conf = configparser.ConfigParser()
conf.read('config.ini')
db = conf["DATABASE"]['dbfile']

app = Flask(__name__)
app.register_blueprint(index.page, url_prefix='/hello')



