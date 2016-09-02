import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) != 3:
    print 'Usage: python client.py <machinename> <port number>'
    sys.exit(0)

machine = sys.argv[1]
port = int (sys.argv[2])

server_address = ( machine, port)
#message = 'This is the message.  It will be repeated.'

try:
    while True:
        userInput = raw_input('> ')
        commandList = userInput.split(' ')
        if commandList[0] == 'quit':
            sock.sendto('quit', server_address)
            print 'Closing socket'
            sock.close()
            sys.exit(0)
        if commandList[0] == 'insert' and len(commandList) == 2:
            print 'Inserted ' + commandList[1]
        message = userInput
        # Send data
        print >>sys.stderr, 'sending "%s"' % message
        sent = sock.sendto(message, server_address)
        
        # Receive response
        print >>sys.stderr, 'waiting to receive'
        data, server = sock.recvfrom(4096)
        ret = ''
        #for chars in data:
        #    ret += chars
        print >>sys.stderr, data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
