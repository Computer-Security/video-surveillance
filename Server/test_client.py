from multiprocessing.connection import Listener
import thread
import requests

# NOTE that this is a demo of communication with server,
# which is NOT finalized code for camera side

def main():
	# maybe use multithreading here
	daemon(True)
	# alert()


def alert():
	# send request to server to alert
	hostname = 'http://127.0.0.1:5000'
	r = requests.get(hostname+'/alert/11')

def activate():
	print 'activate'

def deactivate():
	print 'deactivate'

def daemon(flag):	
	address = ('localhost', 6000)     
	listener = Listener(address, authkey='secret password')
	# listening for message from client: server may send msg to listener camera
	while True:
		conn = listener.accept()
		print 'connection accepted from', listener.last_accepted
		msg = conn.recv()

		if msg == 'activate':
			activate()	
		else:
			deactivate()
			
		conn.close()

	listener.close()


if __name__ == '__main__':
	main()