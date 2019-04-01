from imutils.video.pivideostream import PiVideoStream #Same as the locally made PiVideoStream
import imutils
import time
import cv2

print ("Using camera to find object center")
vs = PiVideoStream().start()
time.sleep(2.0)

while(True):
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] == 0:
            M["m00"] = 1
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "Center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)

    if (cv2.waitKey(1)&0xFF) == ord("q"):
        vs.stop()
        print("Video streaming ended")
        break

vs.stop()