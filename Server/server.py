from flask import Flask, request, Response
from flask import send_file
from flask import jsonify
from multiprocessing.connection import Client
from flask import flash, redirect, render_template, session, abort
# from camera import Camera
import thread
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin  
from flask_sqlalchemy import SQLAlchemy
import user
from dbuser import DBUser
import time
from apns import APNs, Frame, Payload

import os, signal

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


@app.route('/')
def index():
    # return for test
    list = [
        {'param': 'foo', 'val': 2},
        {'param': 'bar', 'val': 10}
    ]
    
    return jsonify(results=list)

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
        uid = validate(username, password)
        if uid:
            # login and validate the user
            user_ = user.User(uid)
            login_user(user_)

            print uid, 'logged in successfully.'
            return jsonify({'result': 'success'})
        else:
            # login fail
            return jsonify({'result': 'fail'})
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

# test code for session
@app.route('/test')
def test():
    if current_user.is_authenticated:
        return Response('''
            <p>success %s</p>
        '''%(current_user.get_id()))
    else:
        return Response('''
            <p>fail</p>
        ''')  

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

def toggleCamera(activate):
    # get pid of camera
    f = open('pid_file', 'rb')
    camera_pid = int(f.readline().strip())
    f.close()
    if activate:
        os.kill(camera_pid, signal.SIGUSR1)
    else:
        os.kill(camera_pid, signal.SIGUSR2)

@app.route('/activate')
def activateCamera():
    # avoid accidental access to /activate to change the status of system
    if current_user.is_authenticated:
        notifyCamera(True)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail'})

@app.route('/deactivate')
def deactivateCamera():
    # avoid accidental access to /deactivate to change the status of system
    if current_user.is_authenticated:
        notifyCamera(False)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail'})

@app.route('/alert/<int:post_id>')
def alert(post_id):
    # magic number
    # avoid accidental access to /alert to alert system
    if post_id == 11:
        try:
            thread.start_new_thread( alertApp, (True, ) )
        except:
            print 'Error: unable to start thread to notify application'
            return 'fail'

    return 'success'

def alertApp(flag):
    apns = APNs(use_sandbox=True, cert_file='CertificatesPush.pem', key_file='key.pem')

    # send a notification to app
    token_hex = '56BAA775284A0CD45606E9DFC4DD278D367BD938A5AD1DCEA527D1027806983A'
    payload = Payload(alert="alert", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)



@app.route('/get_image')
def get_image():
    # send file to client
	filename = 'snapshots/test.jpg'
	return send_file(filename, mimetype = 'image/gif')


# test for camera frame

# def gen(camera):
#     """Video streaming generator function."""
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     Video streaming route
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(host = '0.0.0.0', debug = True)

