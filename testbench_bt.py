from bluetooth import *
import time as t
import sys

#hostMAC = '98:d3:32:10:d7:66'
#hostName = 'EOG_TRANSMITTER'
hostMAC = ''
hostName = ''
port = 8		#8=incoming, 9=outgoing
backlog = 1
size = 1024

nearby_devices = discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))


for addr, name in nearby_devices:
    if name == "EOG_TRANSMITTER":
        print("EOG Controller found")
        print("  %s - %s" % (addr, name))
        hostMAC = addr
        hostName = name
        break

print(find_service())

s = BluetoothSocket(RFCOMM)
s.connect((hostMAC, port))

message = '1'
s.send(message)

while True:
	data = s.recv(1024)
	print('Received', 'data')
	t.sleep(1)

s.close()
