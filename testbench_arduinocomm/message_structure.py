class RCVDMessage():
    __slots__ = ['type', 'id', 'state', 'frontDistance', 'bearings']

class SENDMessage():
    __slots__ = ['type', 'id', 'distance', 'motorspeed', 'motorangle']