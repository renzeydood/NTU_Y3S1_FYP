from message_structure import *

class AnotherTest():
    def __init__(self):
        self.msg2 = RCVDMessage()

    def rcvd(self, data):
        print("This is from rcvd:", id(self.msg2))