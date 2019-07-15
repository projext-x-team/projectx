from flask import Flask
from logging import DEBUG

class Config:
    ENV="dev"
    AppName="Swim Cloud"
    DEFAULT_PAGE_LIMIT = 5
    DB_URI = "sqlite:////Users/alexren/projects/projectX/db"
    #DB_URI = "mysql//"

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'swimcloud'
app.logger.setLevel(DEBUG)