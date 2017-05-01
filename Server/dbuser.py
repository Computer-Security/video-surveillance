'''User model in database'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/user_account.db'
DB = SQLAlchemy(app)


class DBUser(DB.Model):
    '''User model class'''
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True)
    password = DB.Column(DB.String(120), unique=True)

    def __init__(self, username, password):
        '''initialize'''
        self.username = username
        self.password = password

    def __repr__(self):
        '''Return representation of class'''
        return '<User %r>' % self.username


######################################################################
# initialize database from command line:

# from dbuser import db
# from dbuser import DBUser
# db.create_all()
# admin = DBUser('admin', '123456')
# db.session.add(admin)
# db.session.commit()
# users = DBUser.query.all()
# user = DBUser.query.filter_by(username=username).first()
