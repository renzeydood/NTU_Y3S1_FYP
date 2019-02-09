# interfaces the Arduino with the Raspberry Pi
import serial
import time
import serial.tools.list_ports
class ArduinoInterface(object):

	def __init__(self, port, baud_rate):
		#self.port = '/dev/ttyACM0'
		self.port=port
		#self.port='/dev/tty.usbmodem1421'
		self.baudrate = baud_rate
		self.ser = None
		# self.parity= serial.PARITY_ODD
		# self.bytesize=serial.SEVENBITS

	# Start and validate connection to Arduino
	def start_arduino_connection(self):
		print("Initialising Connection to Arduino From Raspberry Pi...")
		try:
			self.ser = serial.Serial(self.port, self.baudrate)
			if (self.ser.isOpen()):
				self.ser.setDTR(False)
				time.sleep(1)
				self.ser.flush()
				self.ser.setDTR(True)
				print("Serial Port: " + self.ser.portstr + " is successfully opened")
				
		except serial.SerialException as e:
			print("Serial Port: {} failed to open. Error: {}".format(self.port, e))

	# Read message from Arduino
	def read_from_arduino(self):
		time.sleep(.001)
		#while True:
		if(self.ser.inWaiting()):
			inByte = self.ser.read()
			print(inByte)
			if(inByte == bytes('~', 'ascii')):
				toReturn = []
				counter = 0
				while True:
					nextByte = self.ser.read()
					print(nextByte)
					counter+=1	
					if(nextByte == bytes('!', 'ascii') and counter == 10):
						#print(toReturn)
						return toReturn
					else:
						toReturn.append(nextByte.decode('ascii'))
		return None
		
	# Write message to Arduino
	def write_to_arduino(self, msg):
		#print("Message to write to arduino: " + msg.decode() )
		try:
			time.sleep(.001)
			self.ser.write(msg)
			self.ser.flush()
			print("Message written successfully")
		except Exception as e:
			print("Error: " + e)
			self.reconnect()

	def end_arduino_connection(self):
		self.ser.close()
		print("Arduino connection closed")
		
	def reconnect(self):
		self.end_arduino_connection() 
		self.start_arduino_connection() 
		print("Reconnecting..") 

def list_ports():
	return [comport.device for comport in serial.tools.list_ports.comports()]
