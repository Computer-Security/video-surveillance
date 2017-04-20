from multiprocessing.connection import Listener
import requests
import signal, os

# NOTE that this is a demo of communication with server,
# which is NOT finalized code for camera side

def activate_handler(signum, frame):
	print 'receive activate msg', signum

def deactivate_handler(signum, frame):
	print 'receive deactivate msg', signum

def main():
	# write pid into file
	f = open('pid_file', 'w')
	f.write(str(os.getpid()))
	f.close()

	# register signal handlers
	signal.signal(signal.SIGUSR1, activate_handler)
	signal.signal(signal.SIGUSR2, deactivate_handler)

	listener()

def alert():
	# send request to server to alert
	hostname = 'http://127.0.0.1:5000'
	r = requests.get(hostname+'/alert/11')

def activate():
	print 'activate'

def deactivate():
	print 'deactivate'

def listener():
	address = ('localhost', 6000)     
	listener = Listener(address, authkey='secret password')
	# listening for message from client: server may send msg to listener camera
	while True:
		print 'listening...'
		conn = listener.accept()
		print 'connection accepted from', listener.last_accepted
		msg = conn.recv()

		if msg == 'activate':
			activate()	
		else:
			deactivate()
			
		conn.close()

	listener.close()
	return 


if __name__ == '__main__':
	main()