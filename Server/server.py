from flask import Flask, request, Response
from flask import send_file
from flask import jsonify
from multiprocessing.connection import Client
# from camera import Camera
import thread

app = Flask(__name__)


@app.route('/')
def index():
    # return for test
    list = [
        {'param': 'foo', 'val': 2},
        {'param': 'bar', 'val': 10}
    ]
    
    return jsonify(results=list)

def notifyCamera(activate):
    # notify the camera using another thread
    try:
       thread.start_new_thread( toggleCamera, (activate, ) )
    except:
       print 'Error: unable to start thread to notify camera'

def toggleCamera(activate):
    # connect to listener camera
    address = ('localhost', 6000)
    conn = Client(address, authkey='secret password')
    if activate:
        conn.send('activate')
    else:
        conn.send('deactivate')
    conn.close()

@app.route('/activate/<int:post_id>')
def activateCamera(post_id):
    # magic number
    # avoid accidental access to /activate to change the status of system
    # should be improved
    if post_id == 11:
        notifyCamera(True)
    return 'activate'

@app.route('/deactivate/<int:post_id>')
def deactivateCamera(post_id):
    # magic number
    # avoid accidental access to /deactivate to change the status of system
    if post_id == 11:
        notifyCamera(False)
    return 'deactivate'

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
    # TODO: send message to app
    return ''


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
	app.run(debug = True, host = '0.0.0.0')

