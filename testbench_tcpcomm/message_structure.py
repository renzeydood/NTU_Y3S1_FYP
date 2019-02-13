ARD_ENC = 'utf-8'
START = '!'
STOP = '~'
MOTOR_CONTROL = '2'
MAX_BYTE_FROM_SERVER = 8 #Includes start and end bytes
MAX_BYTE_FROM_CLIENT = 9 #Includes start and end bytes
DECRYPT_DELAY = '1'

#Arduino to RPi to RPC
class RCVDMessage():
    __slots__ = ['type', 'id', 'state', 'frontDistance', 'bearings']

#RPC to RPi to Arduino
class SENDMessage():
    __slots__ = ['type', 'id', 'distance', 'motorspeed', 'motorangle']