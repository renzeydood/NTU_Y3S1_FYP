from imutils.video.pivideostream import PiVideoStream
from Camera_interface import Camera_interface
from threading import Thread
import cv2

camera = Camera_interface()
camera.connect()

def show_detected_shapes():
    while True:
        """ found = camera.findShapes()

        for shape in found:
            camera.drawShapes(shape) """
        camera.applyFilters()
        camera.display_frame()
        if(cv2.waitKey(1)&0xFF)==ord("q"):
            camera.close()
            print("Video steam ended")
            break

def init_threads():
    display_shape_thread = Thread(target=show_detected_shapes)
    
    display_shape_thread.start()

init_threads()

if __name__ == "__main__":
    print("Camera started")
    """ while True:
        camera.display_frame()
        if(cv2.waitKey(1)&0xFF)==ord("q"):
            camera.close()
            print("Video steam ended")
            break """
