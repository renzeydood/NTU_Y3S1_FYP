from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream #Same as the locally made PiVideoStream
import time
import cv2

print("Start threaded video stream")
vs = PiVideoStream().start()
time.sleep(2.0)

while(True):
    frame = vs.read()
    #frame = cv2.flip(frame, 0)
    cv2.imshow("Frame", frame)
    if(cv2.waitKey(1)&0xFF)==ord("q"):
        vs.stop()
        print("Video steam ended")
        break
 
cv2.destroyAllWindows()
vs.stop()