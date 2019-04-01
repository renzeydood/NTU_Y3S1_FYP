from colordetector import ColorDetector
from scipy.spatial import distance as dist
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
        filters["Gray"], 145, 255, cv2.THRESH_BINARY)[1]
    filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 2)
    filters["Thresh-Adaptive"] = cv2.medianBlur(filters["Thresh-Adaptive"], 5)
    filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
    filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

    return filters[select]


def display_image(img):
    cv2.imshow("Image:", img)
    cv2.waitKey(0)


def segment_bygrabcut(image):
    mask = np.zeros(image.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (132, 57, 230, 141)

    cv2.grabCut(image, mask, rect, bgdModel,
                fgdModel, 15, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    image = image*mask[:, :, np.newaxis]

    return image


def unpickle_shapes(filename):
    pk_in = open(filename, "rb")
    data = pk.load(pk_in)
    pk_in.close()

    return data


def get_contours(img):
    _, cnts, h = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h = h[0]
    return cnts, h


def color_set_original():
    # BGR Format
    clr = {
        "red": [199, 108, 112],
        "green": [134, 175, 132],
        "yellow": [255, 255, 117],
        "white": [255, 255, 255]
    }
    return clr


def color_set():
    # BGR Format
    clr = {
        "red": [182, 48, 66],
        "green": [51, 153, 51],
        "yellow": [255, 255, 0],
        "white": [255, 255, 255]
    }
    return clr


def color_set_lab(clr_set):
    lab = {}

    for clr in clr_set:
        lab[clr] = cv2.cvtColor(np.uint8([[clr_set[clr]]]), cv2.COLOR_RGB2LAB)

    return lab


def compare_euclidean(img, cnt, clr_lab):
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, [cnt], -1, (255, 255, 255), thickness=cv2.FILLED)
    cv2.imshow("Mask", mask)
    cv2.imshow("Image", img)
    
    mask = apply_filter(mask, "Thresh")
    # res = cv2.bitwise_and(image, image, mask=mask)
    mean = cv2.mean(img_lab, mask=mask)[:3]

    print(mean)

    minDist = (np.inf, None)

    for clr in clr_lab:
        d = dist.euclidean(clr_lab[clr], mean)
        print(clr, d)
        if d < minDist[0]:
            minDist = (d, clr)
            
    return minDist[1]


def filter_color(img, cnt, clr, thresh):
    image = img.copy()
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [cnt], -1, (255, 255, 255), thickness=cv2.FILLED)
    mask = apply_filter(mask, "Thresh")
    res = cv2.bitwise_and(image, image, mask=mask)
    

    imageLAB = cv2.cvtColor(res, cv2.COLOR_RGB2LAB)
    lab = cv2.cvtColor(np.uint8([[clr]]), cv2.COLOR_BGR2LAB)[0][0]
    minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
    maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
    val = cv2.inRange(imageLAB, minLAB, maxLAB)

    cv2.imshow("Contour Mask", mask)
    cv2.imshow("Mask Applied", res)
    cv2.imshow("Color Filtered", val)

    cv2.waitKey(0)

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
    # print(res)
    return res
    # return True if res < thresh else False


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
                1.0, set_hu[a_shape][a_hu]) * math.log10(abs(set_hu[a_shape][a_hu]))

    # print(target_hu)
    # print(set_hu)

    print("Difference: ", target_hu - set_hu["arrow_r"])


def imagegethu(filename):
    image = cv2.imread("arrow_modified1.png")
    cnt_ro, h1 = get_contours(apply_filter(image, select="Thresh"))
    cv2.drawContours(image, [cnt_ro[0]], -1, (240, 0, 159), thickness=2)
    print(cv2.moments(cnt_ro[0]))
    cv2.imshow("Image", image)
    cv2.waitKey(0)


def compare_both(set_filtered):
    target_hu = cv2.HuMoments(cv2.moments(set_filtered["arrow_r"])).flatten()
    cnt_ro, h1 = get_contours(apply_filter(
        cv2.imread("arrow_modified1.png"), select="Thresh"))
    rotate_hu = cv2.HuMoments(cv2.moments(cnt_ro[0])).flatten()
    cnt_sc, h2 = get_contours(apply_filter(
        cv2.imread("arrow_modified4.png"), select="Thresh"))
    scale_hu = cv2.HuMoments(cv2.moments(cnt_sc[0])).flatten()
    cnt_sk, h3 = get_contours(apply_filter(
        cv2.imread("arrow_modified3.png"), select="Thresh"))
    skew_hu = cv2.HuMoments(cv2.moments(cnt_sk[0])).flatten()
    cnt_oct, h3 = get_contours(apply_filter(
        cv2.imread("shape_octagon.png"), select="Thresh"))
    octagon_hu = cv2.HuMoments(cv2.moments(cnt_oct[0])).flatten()

    for hu in range(0, 7):
        target_hu[hu] = -1 * \
            math.copysign(1.0, target_hu[hu]) * math.log10(abs(target_hu[hu]))
        rotate_hu[hu] = -1 * \
            math.copysign(1.0, rotate_hu[hu]) * math.log10(abs(rotate_hu[hu]))
        scale_hu[hu] = -1 * \
            math.copysign(1.0, scale_hu[hu]) * math.log10(abs(scale_hu[hu]))
        skew_hu[hu] = -1 * \
            math.copysign(1.0, skew_hu[hu]) * math.log10(abs(skew_hu[hu]))
        octagon_hu[hu] = -1 * \
            math.copysign(1.0, octagon_hu[hu]) * math.log10(abs(octagon_hu[hu]))


    print("Target", target_hu)
    print("Rotate", rotate_hu)
    print("Skew", skew_hu)
    print("Scale", scale_hu)
    print("Octagon", octagon_hu)


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

# ToDo
def get_angle(img, cnts):
    peri = cv2.arcLength(cnts[0], True)
    approx = cv2.approxPolyDP(cnts[0], 0.04 * peri, True)  # 0.04
    print(len(approx))

    print(approx[0][0])
    cv2.line(image, (approx[0][0][0], approx[0][0][1]), (approx[1][0][0], approx[1][0][1]), (0,255,0), 2)
    cv2.line(image, (approx[0][0][0], approx[0][0][1]), (approx[6][0][0], approx[6][0][1]), (0,255,0), 2)
    line1Subtract = np.subtract(approx[0], approx[6])
    line2Subtract = np.subtract(approx[0], approx[1])
    angle1 = math.atan2(line1Subtract[0][1], line1Subtract[0][0])*180/np.pi
    angle2 = math.atan2(line2Subtract[0][1], line2Subtract[0][0])*180/np.pi

    print(angle1, angle2)

    """ cv2.drawContours(img, [approx[0:2]], -1, (159, 240, 0), thickness=2)
    cv2.drawContours(img, [approx[6:9]], -1, (159, 240, 0), thickness=2) """

    cv2.imshow("Result", img)
    cv2.waitKey(0)


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

            angle1 = math.atan2(line1Subtract[0][1], line1Subtract[0][0])*180/np.pi
            angle2 = math.atan2(line2Subtract[0][1], line2Subtract[0][0])*180/np.pi
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
    #clr_lab = color_set_lab(color_set())
    filt_img = apply_filter(img, "Thresh-Adaptive")
    cnts, h = get_contours(filt_img)

    for b, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)  # 0.04

        if cv2.contourArea(c) > 3000 and cv2.contourArea(c) < 30000:

            if ((len(approx) == 8) and compare_withshape(c, shapes_cnts["octagon"], 0.001)):
                if (filter_color(img, c, color_set()["red"], 30)):
                    print("Stop sign detected")
                    cv2.drawContours(img, [approx], -1,(240, 0, 159), thickness=2)

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


def display_cnts(img):
    filt_img = apply_filter(img, "Thresh-Adaptive")

    _, cnts, h = cv2.findContours(filt_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h = h[0]

    for b, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if cv2.contourArea(c) > 1000 and cv2.contourArea(c) < 10000:
            cv2.drawContours(img, [c], -1, (240, 0, 159), thickness=2)
            print("Area of contour: ", cv2.contourArea(c))
            print("Number of lines: ", len(approx))
            print("Contour hierarchy: ", h[b])
    
    cv2.imshow("View", img)
    cv2.waitKey(0)


def image_roi(img):
    roi = img[61:200, 170:310]

    return roi


def compare_humo_image(target_filtered, known_filtered):
    target_hu = cv2.HuMoments(cv2.moments(target_filtered)).flatten()
    known_hu = cv2.HuMoments(cv2.moments(known_filtered)).flatten()

    for hu in range(0, 7):
        target_hu[hu] = -1 * \
            math.copysign(1.0, target_hu[hu]) * math.log10(abs(target_hu[hu]))
        known_hu[hu] = -1 * \
            math.copysign(1.0, known_hu[hu]) * math.log10(abs(known_hu[hu]))

    # print(target_hu)
    # print(set_hu)

    print("Difference: ", target_hu - known_hu)


def nothing(x):
    pass


def color_diff(img, thresh=20):
    image = img.copy()

    panel = np.zeros([100, 700, 3], np.uint8)
    cv2.namedWindow("Panel")

    cv2.createTrackbar("Lower L", "Panel", 0, 179, nothing)
    cv2.createTrackbar("Upper L", "Panel", 179, 179, nothing)
    cv2.createTrackbar("Lower A", "Panel", 0, 255, nothing)
    cv2.createTrackbar("Upper A", "Panel", 255, 255, nothing)
    cv2.createTrackbar("Lower B", "Panel", 0, 255, nothing)
    cv2.createTrackbar("Upper B", "Panel", 255, 255, nothing)

    while (1):
        l_l = cv2.getTrackbarPos("Lower L", "Panel")
        u_l = cv2.getTrackbarPos("Upper L", "Panel")
        l_a = cv2.getTrackbarPos("Lower A", "Panel")
        u_a = cv2.getTrackbarPos("Upper A", "Panel")
        l_b = cv2.getTrackbarPos("Lower B", "Panel")
        u_b = cv2.getTrackbarPos("Upper B", "Panel")

        imageLAB = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        # lab = cv2.cvtColor(np.uint8([[clr]]), cv2.COLOR_BGR2LAB)[0][0]
        # minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
        # maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
        minLAB = np.array([l_l, l_a, l_b])
        maxLAB = np.array([u_l, u_a, u_b])
        val = cv2.inRange(imageLAB, minLAB, maxLAB)

        cv2.imshow("Panel", panel)
        cv2.imshow("Result", val)

    return np.any(val), val

if __name__ == "__main__":
    shapes_cnts = unpickle_shapes("shape_templates/shapeset_cnts")

    
    image = get_image()

    #display_image(apply_filter(image, "Thresh-Adaptive"))

    display_cnts(image)

    
