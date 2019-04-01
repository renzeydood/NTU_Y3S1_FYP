import imutils
import cv2
import numpy as np
import pickle as pk

def apply_filter(img, select="Gray"):
    filters = {}
    output = img.copy()

    filters["Original"] = output
    filters["Blur"] = cv2.GaussianBlur(output, (3, 3), 0)
    filters["Gray"] = cv2.cvtColor(filters["Blur"], cv2.COLOR_BGR2GRAY)
    filters["Thresh"] = cv2.threshold(filters["Gray"], 113, 255, cv2.THRESH_BINARY)[1]#60
    filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
    filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

    return filters[select]

def shapes_set_img():
    set = {
        "arrow_r" : apply_filter(cv2.imread("arrow_r.png"), "Thresh"),
        "circle" : apply_filter(cv2.imread("circle.png"), "Thresh"),
        "diamond" : apply_filter(cv2.imread("diamond.png"), "Thresh"),
        "octagon" : apply_filter(cv2.imread("octagon.png"), "Thresh")
    }

    return set

def shapes_set_cnts(shapes_img):
    shape_cnt = {}

    for shape in shapes_img:
        curr_shape = shapes_img[shape]
        cnts = cv2.findContours(curr_shape, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        shape_cnt[shape] = cnts[0]

    return shape_cnt

def color_set():
    clr = {
        "red" : [199, 108, 112],
        "green" : [134, 175, 132],
        "yellow" : [255, 255, 117],
        "white" : [255, 255, 255]
    }
    return clr

def color_set_lab(clr_set):
    lab = {}

    for clr in clr_set:
        lab[clr] = cv2.cvtColor(np.uint8([[clr_set[clr]]]), cv2.COLOR_BGR2LAB)[0][0]
    return lab

def pickle(name, data):
    pk_out = open(name, "wb")
    pk.dump(data, pk_out, protocol=2)
    pk_out.close()

def unpickle(filename):
    pk_in = open(filename, "rb")
    data = pk.load(pk_in)

    return data

if __name__ == "__main__":
    pickle("shapeset_img", shapes_set_img())
    pickle("shapeset_cnts", shapes_set_cnts(shapes_set_img()))
    pickle("colorset_arr", color_set())
    pickle("colorset_lab", color_set_lab(color_set()))
    
    print("Serialization done!")
    pass