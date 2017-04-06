from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/user_account.db'
db = SQLAlchemy(app)


class DBUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


######################################################################
# initialize database from command line:

# from dbuser import db
# from dbuser import DBUser
# admin = DBUser('admin', '123456')
# db.session.add(admin)
# db.session.commit()
# users = DBUser.query.all()
# user = DBUser.query.filter_by(username=username).first()
