"""Server controlling camera script,
receive requests from user app
"""
import thread
import re
import os
import signal
import cgi
import subprocess
from flask import Flask, request, Response
from flask import jsonify
from flask_login import LoginManager, login_required, login_user
from flask_login import logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import user
from dbuser import DBUser


# create login manager
LOGIN_MANAGER = LoginManager()

# create app object
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/user_account.db'
DB = SQLAlchemy(app)

# configure login manager
LOGIN_MANAGER.init_app(app)

# process for camera control
CAMERA_PROC = None

@app.route('/')
def index():
    """index page"""
    return "hello world"

def sanitize(inputstr):
    """Return user input after sanitation"""
    # remove punctuation
    inputstr = inputstr.strip()
    # convert charaters '&', '<', '>' to HTML-safe sequences
    transformed = cgi.escape(inputstr)
    # check if input is valid
    if not re.match("^[a-zA-Z0-9_]*$", inputstr):
        return None
    return transformed

def validate(username, pwd):
    """Return retrieved user from database"""
    user_ = DBUser.query.filter_by(username=username).first()
    # plain text password
    if user_ and user_.password == pwd:
        return unicode(user_.id)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Return log in status message"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        username_ = sanitize(username)
        password_ = sanitize(password)

        if username_ is None or password_ is None:
            return jsonify({'result': 'fail', 'error': 'input not valid'})

        uid = validate(username_, password_)
        if uid:
            # login and validate the user
            user_ = user.User(uid)
            login_user(user_)

            print uid, 'logged in successfully.'
            return jsonify({'result': 'success', 'error': ''})
        # login fail
        return jsonify({'result': 'fail', 'error': 'no user found'})
    else:
        # for test
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>''')

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """Return loaded user"""
    print 'loading user', user_id
    return user.User(user_id)

@app.route("/logout")
@login_required
def logout():
    """Return log out status"""
    logout_user()
    return jsonify({'result': 'success'})

def notify_camera(activate):
    """Notify the camera using another thread"""
    try:
        thread.start_new_thread(toggle_camera, (activate, ))
    except:
        print 'Error: unable to start thread to notify camera'
        return False
    return True

def toggle_camera(activate):
    """Notify the camera of activation/deactivation message"""
    global CAMERA_PROC
    if activate:
        if CAMERA_PROC:
            # send signal for activating motion detection
            os.kill(CAMERA_PROC.pid, signal.SIGUSR1)
    else:
        if CAMERA_PROC:
            # send signal for deactivating motion detection
            os.kill(CAMERA_PROC.pid, signal.SIGUSR2)

@app.route('/activate')
def activate_camera():
    """Return status of activating camera"""
    # avoid accidental access to /activate to change the status of system
    if current_user.is_authenticated:
        res = notify_camera(True)
        if res:
            return jsonify({'result': 'success'})
    return jsonify({'result': 'fail'})

@app.route('/deactivate')
def deactivate_camera():
    """Return status of deactivating camera"""
    # avoid accidental access to /deactivate to change the status of system
    if current_user.is_authenticated:
        res = notify_camera(False)
        if res:
            return jsonify({'result': 'success'})
    return jsonify({'result': 'fail'})

if __name__ == '__main__':
    app.secret_key = 'secret_key'
     # open a subprocess of camera running
    CAMERA_PROC = subprocess.Popen(['python', 'pi_surveillance.py', '--conf', 'conf.json'])
    app.run(host='0.0.0.0', port='8280')
