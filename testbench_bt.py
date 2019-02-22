import bluetooth

#hostMAC = '98:d3:32:10:d7:66'
#hostName = 'EOG_TRANSMITTER'
hostMAC = ''
hostName = ''
port = 3 
backlog = 1
size = 1024

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    if name == "EOG_TRANSMITTER":
        print("EOG Controller found")
        print("  %s - %s" % (addr, name))
        hostMAC = addr
        hostName = name
        break

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMAC, port))
s.listen(backlog)
try:
	client, clientInfo = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data) # Echo back to client
except:	
	print("Closing socket")
	client.close()
s.close()

