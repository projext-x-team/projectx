from flask import Flask
from logging import DEBUG

class Config:
    ENV="dev"
    AppName="Swim Cloud"
    DEFAULT_PAGE_LIMIT = 5
    # Alex's local DB
    DB_URI = "sqlite:////Users/alexren/projects/projectX/db"
    # John's local DB
    # DB_URI = "sqlite:////Users/huang/Documents/_Workspace/projectx/db"
    # Production DB
    # DB_URI = "postgres://bmccpkxvfniseh:d2103f913c6848c73a5d01282e9ee392d2d3320f74ce0eec2deb0d4463916fad@ec2-174-129-227-80.compute-1.amazonaws.com:5432/d2kv5ln1qmovdo"


app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'swimcloud'
app.logger.setLevel(DEBUG)