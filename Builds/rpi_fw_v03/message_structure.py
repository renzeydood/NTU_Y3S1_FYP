ARD_ENC = 'utf-8'
START = '!'
STOP = '~'
CR = '\r'
MOTOR_CONTROL = '2'
MAX_BYTE_FROM_SERVER = 8  # Includes start and end bytes (RCVD)
MAX_BYTE_FROM_CLIENT = 9  # Includes start and end bytes (SEND)
DECRYPT_DELAY = '1'


def int_to_bytes(data):
    return chr(data >> 7) + chr(data & 0x7F)


def bytes_to_int(u, l):
    return u << 7 | l

# Arduino to RPi to RPC


class RCVDMessage():
    def __init__(self):
        self.type = 0
        self.id = 0
        self.state = 0
        self.frontDistance = 0
        self.bearings = 0

    def destruct(self, data):
        self.type = data[0]
        self.id = ord(data[1])
        self.state = data[2]
        self.frontDistance = bytes_to_int(ord(data[3]), ord(data[4]))
        self.bearings = bytes_to_int(ord(data[5]), ord(data[6]))
        return self


# RPC to RPi to Arduino
class SENDMessage():
    def __init__(self):
        self.type = b'\x00'.decode()
        self.id = 0
        self.distance = 0
        self.motorspeed = 0
        self.motorangle = 0

    def construct(self):
        return (START + self.type + chr(self.id) + int_to_bytes(self.distance) + int_to_bytes(self.motorspeed) + int_to_bytes(self.motorangle) + STOP + CR).encode()
