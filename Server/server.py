from flask import Flask, request, Response
from flask import jsonify
from multiprocessing.connection import Client
from flask import flash, redirect, render_template, session, abort
import thread
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin  
from flask_sqlalchemy import SQLAlchemy
import user
from dbuser import DBUser
import time

import os, signal
import subprocess
import cgi
import re

# create login manager
login_manager = LoginManager()

# create app object
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/user_account.db'
db = SQLAlchemy(app)

# configure login manager
login_manager.init_app(app)

# process for camera control
camera_proc = None

@app.route('/')
def index():
    return "hello world"

def sanitize(inputstr):
    # remove punctuation
    inputstr = inputstr.strip()
    # convert charaters '&', '<', '>' to HTML-safe sequences
    transformed = cgi.escape(inputstr)
    # check if input is valid
    if not re.match("^[a-zA-Z0-9_]*$", inputstr):
        return None
    return transformed

def validate(username, pwd):
    user = DBUser.query.filter_by(username=username).first()
    # plain text password
    if user and user.password == pwd:
        return unicode(user.id)
    else:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        username_ = sanitize(username)
        password_ = sanitize(password)

        if username_ == None or password_ == None:
            return jsonify({'result': 'fail', 'error': 'input not valid'}) 

        uid = validate(username_, password_)
        if uid:
            # login and validate the user
            user_ = user.User(uid)
            login_user(user_)

            print uid, 'logged in successfully.'
            return jsonify({'result': 'success', 'error': ''})
        else:
            # login fail
            return jsonify({'result': 'fail', 'error': 'no user found'})
    else:
        # for test
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''') 

@login_manager.user_loader
def load_user(user_id):
    print 'loading user', user_id
    return user.User(user_id)
    # use session id instead of user id to identify users
    # return User.query.filter_by(session_token=session_token).first()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({'result': 'success'})

def notifyCamera(activate):
    # notify the camera using another thread
    try:
        thread.start_new_thread( toggleCamera, (activate, ) )
    except:
        print 'Error: unable to start thread to notify camera'
        return False
    return True

def toggleCamera(activate):
    global camera_proc
    if activate:
        if camera_proc:
            # send signal for activating motion detection
            os.kill(camera_proc.pid, signal.SIGUSR1)
    else:
        if camera_proc:
            # send signal for deactivating motion detection
            os.kill(camera_proc.pid, signal.SIGUSR2)

@app.route('/activate')
def activateCamera():
    # avoid accidental access to /activate to change the status of system
    if current_user.is_authenticated:
        res = notifyCamera(True)
        if res:
            return jsonify({'result': 'success'})
    
    return jsonify({'result': 'fail'})

@app.route('/deactivate')
def deactivateCamera():
    # avoid accidental access to /deactivate to change the status of system
    if current_user.is_authenticated:
        res = notifyCamera(False)
        if res:
            return jsonify({'result': 'success'})

    return jsonify({'result': 'fail'})

@app.route('/get_image')
def get_image():
    # send file to client
	filename = 'snapshots/test.jpg'
	return send_file(filename, mimetype = 'image/gif')


if __name__ == '__main__':
    app.secret_key = 'secret_key'
     # open a subprocess of camera running
    camera_proc = subprocess.Popen(['python', 'pi_surveillance.py', '--conf', 'conf.json'])
    app.run(host = '0.0.0.0', port = '8280')

