import imutils
import cv2
import numpy as np

class DataSet():
    def __init__(self):
        self.clrset_rgb = self.color_set()
        self.clrset_lab = self.color_set_lab(self.clrset_rgb)
        self.shapeset_img = self.shapes_set_img()
        self.shapeset_cnt = self.shapes_set_cnts(self.shapeset_img)

    def apply_filter(self, img, select="Gray"):
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

    def shapes_set_img(self):
        img_set = {
            "arrow_r" : self.apply_filter(cv2.imread("shape_templates/arrow_r.png"), "Thresh"),
            "circle" : self.apply_filter(cv2.imread("shape_templates/circle.png"), "Thresh"),
            "diamond" : self.apply_filter(cv2.imread("shape_templates/diamond.png"), "Thresh"),
            "octagon" : self.apply_filter(cv2.imread("shape_templates/octagon.png"), "Thresh")
        }

        return img_set

    def shapes_set_cnts(self, shapes_img):
        shape_cnt = {}

        for shape in shapes_img:
            curr_shape = shapes_img[shape]
            cnts = cv2.findContours(curr_shape, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            shape_cnt[shape] = cnts[0]

        return shape_cnt

    def color_set(self):
        clr = {
            "red" : [199, 108, 112],
            "green" : [134, 175, 132],
            "yellow" : [255, 255, 117],
            "white" : [255, 255, 255]
        }
        return clr

    def color_set_lab(self, clr_set):
        lab = {}

        for clr in clr_set:
            lab[clr] = cv2.cvtColor(np.uint8([[clr_set[clr]]]), cv2.COLOR_BGR2LAB)[0][0]
        return lab