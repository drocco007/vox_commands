import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)

# socket.bind("tcp://*:5557")
socket.connect('tcp://vmhost:5555')


def on_state_change(change_type, argument):
	# print __name__, 'on_state_change:', change_type, argument

	socket.send('{}{} {}'.format('\x01', change_type, argument))

def unload():
    socket.close()
