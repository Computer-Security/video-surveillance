"""USAGE
   python pi_surveillance.py --conf conf.json
"""
# import the necessary packages
import subprocess
import signal
import json
import time
import argparse
import warnings
import datetime
from pyimagesearch.tempimage import TempImage
from dropbox.client import DropboxOAuth2FlowNoRedirect
from dropbox.client import DropboxClient
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import imutils
import cv2

import push_notification

MOTION_DETECT_ON = True

def __alert__():
	# send request to server to alert
    push_notification.alert()

def __activate_handler__(signum):
    print 'receive activate msg', signum
    global MOTION_DETECT_ON
    MOTION_DETECT_ON = True

def __deactivate_handler__(signum):
    print 'receive deactivate msg', signum
    global MOTION_DETECT_ON
    MOTION_DETECT_ON = False

# register signal handlers
signal.signal(signal.SIGUSR1, __activate_handler__)
signal.signal(signal.SIGUSR2, __deactivate_handler__)

# construct the argument parser and parse the arguments
AP = argparse.ArgumentParser()
AP.add_argument("-c", "--conf", required=True,
	               help="path to the JSON configuration file")
ARGS = vars(AP.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
CONF = json.load(open(ARGS["conf"]))
CLIENT = None

# check to see if the Dropbox should be used
if CONF["use_dropbox"]:
	# connect to dropbox and start the session authorization process
    FLOW = DropboxOAuth2FlowNoRedirect(CONF["dropbox_key"], CONF["dropbox_secret"])
    print "[INFO] Authorize this application: {}".format(FLOW.start())

    AUTH_CODE = raw_input("Enter auth code here: ").strip()

	# finish the authorization and grab the Dropbox client
    (ACCESS_TOKEN, USER_ID) = FLOW.finish(AUTH_CODE)
    CLIENT = DropboxClient(ACCESS_TOKEN)
    print "[SUCCESS] dropbox account linked"

# initialize the camera and grab a reference to the raw camera capture
CAMERA = PiCamera()
CAMERA.resolution = tuple(CONF["resolution"])
CAMERA.framerate = CONF["fps"]
RAW_CAPTURE = PiRGBArray(CAMERA, size=tuple(CONF["resolution"]))

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] warming up..."
time.sleep(CONF["camera_warmup_time"])
AVG = None
LAST_UPLOADED = datetime.datetime.now()
MOTION_COUNTER = 0

STREAM = picamera.PiCameraCircularIO(CAMERA, seconds=20)
CAMERA.start_recording(STREAM, format='h264', quality=23)

# set up vlc subprocess for streaming
CMDLINE = ['cvlc', '-vvv', 'stream:///dev/stdin',
           '--sout', '#standard{access=http,mux=ts,dst=192.168.0.8:8160}',
           ':demux=h264'
          ]
STREAMER = subprocess.Popen(CMDLINE, stdin=subprocess.PIPE)

POS = None
STREAM_INTERVAL = 0.1
DETECTION_INTERVAL = 0.1
COUNT = 0
print 'Start streaming'
while True:
    CAMERA.wait_recording(STREAM_INTERVAL)
    with STREAM.lock:
        if POS:
            STREAM.seek(POS)
            DATA = STREAM.read()
            #print "Stream End Position:   ", stream.tell()
            #print "Streaming Data size:   ", len(data)
            STREAMER.stdin.write(DATA)

        POWER = STREAM.tell()
        #print "Stream Start Position: ", pos

        COUNT = (COUNT+1) % (int(DETECTION_INTERVAL / STREAM_INTERVAL))
    if (not MOTION_DETECT_ON) or (COUNT != 0):
        continue

    # capture frames from the camera
    CAMERA.capture(RAW_CAPTURE, format="bgr", use_video_port=True)
    # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
    FRAME = RAW_CAPTURE.array
    TIMESTAMP = datetime.datetime.now()
    TEXT = "Unoccupied"

    # resize the frame, convert it to grayscale, and blur it
    FRAME = imutils.resize(FRAME, width=500)
    GRAY = cv2.cvtColor(FRAME, cv2.COLOR_BGR2GRAY)
    GRAY = cv2.GaussianBlur(GRAY, (21, 21), 0)

    # if the average frame is None, initialize it
    if AVG is None:
        print "[INFO] starting background model..."
        AVG = GRAY.copy().astype("float")
        RAW_CAPTURE.truncate(0)
        continue

	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
    cv2.accumulateWeighted(GRAY, AVG, 0.5)
    FRAME_DELTA = cv2.absdiff(GRAY, cv2.convertScaleAbs(AVG))

    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    THRESH = cv2.threshold(FRAME_DELTA, CONF["delta_thresh"], 255,
                           cv2.THRESH_BINARY)[1]
    THRESH = cv2.dilate(THRESH, None, iterations=2)
    (_, CNTS, _) = cv2.findContours(THRESH.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in CNTS:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < CONF["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(FRAME, (x, y), (x + w, y + h), (0, 255, 0), 2)
        TEXT = "Occupied"

    # draw the text and timestamp on the frame
    TS = TIMESTAMP.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(FRAME, "Room Status: {}".format(TEXT), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(FRAME, TS, (10, FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # check to see if the room is occupied
    if TEXT == "Occupied":
        __alert__()
        # check to see if enough time has passed between uploads
        if (TIMESTAMP - LAST_UPLOADED).seconds >= CONF["min_upload_seconds"]:
            # increment the motion counter
            MOTION_COUNTER += 1

            # check to see if the number of frames with consistent motion is high enough
            if MOTION_COUNTER >= CONF["min_motion_frames"]:
                # check to see if dropbox sohuld be used
                if CONF["use_dropbox"]:
                    # write the image to temporary file
                    T = TempImage()
                    cv2.imwrite(T.path, FRAME)

                    # upload the image to Dropbox and cleanup the tempory image
                    print "[UPLOAD] {}".format(TS)
                    PATH = "{base_path}/{timestamp}.jpg".format(
                        base_path=CONF["dropbox_base_path"], timestamp=TS)
                    CLIENT.put_file(PATH, open(T.path, "rb"))
                    T.cleanup()

                # update the last uploaded timestamp and reset the motion
                # counter
                LAST_UPLOADED = TIMESTAMP
                MOTION_COUNTER = 0

    # otherwise, the room is not occupied
    else:
        MOTION_COUNTER = 0

    # check to see if the frames should be displayed to screen
    if CONF["show_video"]:
        # display the security feed

        cv2.imshow("Security Feed", FRAME)
        KEY = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if KEY == ord("q"):
            break
    # clear the stream in preparation for the next frame
    RAW_CAPTURE.truncate(0)

print 'The end'
CAMERA.stop_recording()
STREAMER.terminate()
