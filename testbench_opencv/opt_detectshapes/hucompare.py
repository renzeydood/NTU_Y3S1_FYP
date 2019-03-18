from colordetector import ColorDetector
import argparse
import imutils
import cv2
import numpy as np
import math
import pickle as pk


def get_image():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    args = vars(ap.parse_args())

    return cv2.imread(args["image"])


def apply_filter(img, select="Gray"):
    filters = {}
    output = img.copy()

    filters["Original"] = output
    filters["Blur"] = cv2.GaussianBlur(output, (7, 7), 0)
    filters["Gray"] = cv2.cvtColor(filters["Blur"], cv2.COLOR_BGR2GRAY)
    filters["Thresh"] = cv2.threshold(
        filters["Gray"], 145, 255, cv2.THRESH_BINARY)[1]  # 60
    filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(
        filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
    filters["Thresh-Adaptive"] = cv2.erode(
        filters["Thresh-Adaptive"], None, iterations=0)
    filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
    filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

    return filters[select]


def display_image(img):
    cv2.imshow("Image:", img)
    cv2.waitKey(0)


def unpickle_shapes(filename):
    pk_in = open(filename, "rb")
    data = pk.load(pk_in)

    return data


def get_contours(img):
    cnts = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts


def color_set():
    clr = {
        "red": [199, 108, 112],
        "green": [134, 175, 132],
        "yellow": [255, 255, 117],
        "white": [255, 255, 255]
    }
    return clr


def filter_color(img, cnt, clr, thresh):
    image = img.copy()
    mask = np.zeros(image.shape, np.uint8)
    cv2.imshow("mask", mask)
    cv2.drawContours(mask, [cnt], -1, (255, 255, 255), thickness=cv2.FILLED)
    mask = apply_filter(mask, "Thresh")
    res = cv2.bitwise_and(image, image, mask=mask)

    imageLAB = cv2.cvtColor(res, cv2.COLOR_RGB2LAB)
    lab = cv2.cvtColor(np.uint8([[clr]]), cv2.COLOR_BGR2LAB)[0][0]
    minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
    maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
    val = cv2.inRange(imageLAB, minLAB, maxLAB)
    return np.any(val), val


def filter_color_nocnts(img, clr, thresh):
    image = img.copy()

    imageLAB = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    lab = cv2.cvtColor(np.uint8([[clr]]), cv2.COLOR_BGR2LAB)[0][0]
    minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
    maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
    val = cv2.inRange(imageLAB, minLAB, maxLAB)

    cv2.imshow("Filtered", val)
    cv2.waitKey(0)


def compare_withset(target, set, thresh):
    result = {}

    for shape in set:
        res = cv2.matchShapes(target, set[shape], cv2.CONTOURS_MATCH_I3, 0)
        result[shape] = res
        print("Comparing with: ", shape, ", Value: ", res)

    guessshape = min(result, key=result.get)

    return guessshape if result[guessshape] < thresh else "Not found"


def compare_withshape(target, shape, thresh):
    res = cv2.matchShapes(target, shape, cv2.CONTOURS_MATCH_I3, 0)
    return True if res < thresh else False


def compare_humo(target_filtered, set_filtered):
    target_hu = cv2.HuMoments(cv2.moments(target_filtered)).flatten()
    set_hu = {}

    for shape in set_filtered:
        set_hu[shape] = cv2.HuMoments(
            cv2.moments(set_filtered[shape])).flatten()

    for hu in range(0, 7):
        target_hu[hu] = -1 * \
            math.copysign(1.0, target_hu[hu]) * math.log10(abs(target_hu[hu]))

    for a_shape in set_hu:
        for a_hu in range(0, 7):
            set_hu[a_shape][a_hu] = -1 * math.copysign(
                1.0, set_hu[a_shape][a_hu]) * m.log10(abs(set_hu[a_shape][a_hu]))

    # print(target_hu)
    # print(set_hu)

    print("Difference: ", target_hu - set_hu["arrow_r"])


def checkInRange(value, lower, upper):
    if lower <= value <= upper:
        return True
    return False


def angleToTipOrientation(anglePair):
    tolerance = 10
    if checkInRange(anglePair[0], 135-tolerance, 135+tolerance) and checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance)):  # 135 && -135
        return "Left"
    elif checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance)) and checkInRange(anglePair[1], 45-tolerance, 45+tolerance):  # -45 && 45
        return "Right"
    elif checkInRange(anglePair[0], -(135+tolerance), -(135-tolerance)) and checkInRange(anglePair[1], -(45+tolerance), -(45-tolerance)):  # -135 && -45
        return "Up"
    elif checkInRange(anglePair[0], 45-tolerance, 45+tolerance) and checkInRange(anglePair[1], 135-tolerance, 135+tolerance):  # 45 && 135
        return "Down"
    else:
        return None


def findArrow(c, approx):
    potentialArrowOrient = None
    rightAngleCounter = 0

    if len(approx) == 7:
        for index, m in enumerate(approx):
            if index == 0:
                line1Subtract = np.subtract(m, approx[6])
                line2Subtract = np.subtract(m, approx[1])
            elif index == 6:
                line1Subtract = np.subtract(m, approx[5])
                line2Subtract = np.subtract(m, approx[0])
            else:
                line1Subtract = np.subtract(m, approx[index - 1])
                line2Subtract = np.subtract(m, approx[index + 1])

            angle1 = math.atan2(
                line1Subtract[0][1], line1Subtract[0][0])*180/np.pi
            angle2 = math.atan2(
                line2Subtract[0][1], line2Subtract[0][0])*180/np.pi
            tipOrientation = angleToTipOrientation((angle1, angle2))
            potentialArrowOrient = potentialArrowOrient if tipOrientation is None else tipOrientation
            ptAngle = abs(angle1 + angle2)

            if abs(ptAngle) < 25 or abs(ptAngle - 90) < 25 or abs(ptAngle - 180) < 25 or abs(ptAngle - 270) < 25:
                rightAngleCounter += 1

    if(rightAngleCounter == 5 and potentialArrowOrient is not None):
        # self.drawShapes(c, potentialArrowOrient, approx[0][0])
        # if cv2.contourArea(c) > 12000:
        return potentialArrowOrient

    return None


def get_shape(img):
    shapes_cnts = unpickle_shapes("database/shapeset_cnts")
    clr_lab = unpickle_shapes("database/colorset_lab")
    filt_img = apply_filter(img, "Thresh-Adaptive")
    #img_cnts = get_contours(filt_img)

    _, cnts, h = cv2.findContours(
        filt_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h = h[0]

    for b, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)  # 0.04

        if cv2.contourArea(c) > 400 and cv2.contourArea(c) < 10000:

            if ((len(approx) == 8) and compare_withshape(c, shapes_cnts["octagon"], 0.001)):
                if (filter_color(img, c, color_set()["red"], 20)):
                    print("Stop sign detected")
                    cv2.drawContours(img, [approx], -1,
                                     (240, 0, 159), thickness=2)

            elif ((len(approx) == 4) and compare_withshape(c, shapes_cnts["diamond"], 0.002)):
                if (filter_color(img, c, color_set()["yellow"], 20)):
                    print("Slow sign detected")
                    cv2.drawContours(img, [approx], -1,
                                     (240, 0, 159), thickness=2)

            elif (compare_withshape(c, shapes_cnts["circle"], 0.001)):
                is_red, inner_red = filter_color(
                    img, c, color_set()["red"], 20)
                is_green, inner_green = filter_color(
                    img, c, color_set()["green"], 20)

                if(is_red):
                    print("Traffic light: Red detected")

                elif(is_green):
                    if(h[b, 2] != -1):
                        print("Child exist")
                        _, ar = (filter_color(
                            img, c, color_set()["white"], 20))
                        ar_c = get_contours(ar)
                        for c_in in ar_c:
                            peri_in = cv2.arcLength(c_in, True)
                            approx_in = cv2.approxPolyDP(
                                c_in, 0.04 * peri_in, True)  # 0.04
                            print("Traffic light: Green with {} arrow detected".format(
                                findArrow(ar_c, approx_in)))
                            cv2.drawContours(
                                img, [c_in], -1, (240, 0, 159), thickness=2)

                cv2.drawContours(img, [c], -1, (240, 0, 159), thickness=2)

            elif ((len(approx) == 7)):
                if(filter_color(img, c, color_set()["white"], 20)):
                    ar = findArrow(c, approx)
                    print("{} arrow sign detected".format(ar))
                    cv2.drawContours(img, [c], -1, (240, 0, 159), thickness=2)

            cv2.imshow("View", img)
            cv2.waitKey(0)


if __name__ == "__main__":
    shapes_cnts = unpickle_shapes("shape_templates/shapeset_cnts")
    image = get_image()

    # get_shape(image)
    filter_color_nocnts(image, color_set()["white"], 80)
