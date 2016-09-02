import socket
import sys
import taxonomy

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) != 2:
    print 'Usage: python server.py <port number>'
    sys.exit(0)

portNum = int(sys.argv[1])

# Bind the socket to the port
server_address = ('nike.cs.uga.edu', portNum)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
tester = taxonomy.Taxonomy('')
while True:
    #print >>sys.stderr, '\nwasiting to receive message'
    data, address = sock.recvfrom(4096)
    
    print >>sys.stderr, 'received %s bytes from %s' % (data, address)
    print >>sys.stderr, data

    commandList = data.split(' ')
    for str in commandList:
        print str

    if commandList[0] == 'insert' and len(commandList) == 2:
        tester.insert(commandList[1])
        # sent = sock.sendto('Inserted ' + data, address)
    elif commandList[0] == 'list':
        sent = sock.sendto(tester.list(), address)
    elif commandList[0] == 'quit':
        print 'Terminating the server.'
        sock.close()
        sys.exit(0)
    else:
        print 'The command ' + commandList[0] + ' is not supported'
    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
