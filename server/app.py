from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database_file = "sqlite:////Users/alexren/projects/projectX/db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class US_Rankings(db.Model):
    __tablename__ = 'US_Rankings'
    id = db.Column(db.BigInteger, primary_key = True)
    swimmer = db.Column(db.Text)
    age = db.Column(db.BigInteger)
    lsc = db.Column(db.Text)
    club = db.Column(db.Text)
    time = db.Column(db.Float)
    date = db.Column(db.Text)
    swim_meet = db.Column(db.Text)

    def __repr__(self):
        return "<US_Rankings: {}>".format(self.swimmer)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()