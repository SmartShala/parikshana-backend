from typing import OrderedDict
from imutils.perspective import four_point_transform
import numpy as np
import imutils
from imutils import contours
import cv2
import easyocr

# ------------Class for extracting answers-----------------


class Sheet:
    def __init__(self, img):
        if __name__ == ("__main__"):
            self.original = cv2.imread(img)
        else:
            # read image as an numpy array
            self.original = np.asarray(bytearray(img), dtype="uint8")
            # use imdecode function
            self.original = cv2.imdecode(self.original, cv2.IMREAD_COLOR)
        self.student_id = None
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)  # Grayscale image
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
        self.warped = self.warpImage(edged)
        thresh = self.threshed(self.warped, 50)
        # self.show(thresh, "THresh")
        self.text_boxes = self.getTextArea(self.warped)
        questionCnts = self.getBoxContours(thresh)
        self.box_contour_img = self.warped.copy()
        cv2.drawContours(self.box_contour_img, questionCnts, -1, (0, 255, 0), 2)
        # self.show(self.box_contour_img, "Box Contours")
        # cv2.imshow("Contours",cv2.resize(cont, None, fx=0.4, fy=0.4))
        # cv2.imwrite("processed_si.jpeg",cont)
        boxes = self.separateBoxes(self.box_contour_img, 20)
        self.answerlist = {}
        second = False

        # ------------iterating through each box-------------

        for box in boxes:
            boxmask = self.maskBoxImage(self.crop, box)
            boxmask = self.threshed(boxmask, 86)
            cnts = self.answerBoxContours(boxmask)
            self.answerlist = self.getAnswers(boxmask, cnts, second, self.answerlist)
            second = not second
        self.answerlist = OrderedDict(sorted(self.answerlist.items()))
        # cv2.waitKey(0)

    # -------------Cropping and warping image to fit the border--------
    def warpImage(self, img):
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        docCnt = None

        # ensure that at least one contour was found
        if len(cnts) > 0:
            # sort the contours according to their size in
            # descending order
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            # loop over the sorted contours
            for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                # if our approximated contour has four points,
                # then we can assume we have found the border
                if len(approx) == 4:
                    docCnt = approx
                    break

        # apply a four point perspective transform to both the
        # original image and grayscale image to obtain a top-down
        # birds eye view of the paper
        original = four_point_transform(self.original, docCnt.reshape(4, 2))
        warped = four_point_transform(self.gray, docCnt.reshape(4, 2))
        return warped

    # -----------Resizes image to fit the screen---------
    def resized(self, img):
        return cv2.resize(img, None, fx=0.4, fy=0.4)

    # ---------Shows image on screen-----------
    def show(self, img, x=""):
        cv2.imshow(x, self.resized(img))

    # ---------Returns image after thresholding-------------
    def threshed(self, img, val):
        res = cv2.threshold(img, val, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        return res

    # -------------Grabs all boxes in the page---------------
    def getBoxContours(self, img):
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        # loop over the contours
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            # only takes the boxes with below criterias
            if w >= 20 and h >= 20 and w / h < 2:
                questionCnts.append(c)
        return questionCnts

    # -----------------Separates the two boxes of answers------------
    def separateBoxes(self, img, crop_f):
        self.crop = img[crop_f : img.shape[0] - crop_f, crop_f : img.shape[1] - crop_f]
        thres = self.threshed(self.crop, 150)
        # show(thres, "thres")

        cnts = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        # print(len(cnts))

        # takes the two biggest boxes
        bigboiboxes = sorted(cnts, key=cv2.contourArea, reverse=True)[0:2]
        return bigboiboxes

    # --------------returns a mask with only the current box-------------
    def maskBoxImage(self, img, boi):

        mask = np.zeros(img.shape, dtype="uint8")
        cv2.drawContours(mask, boi, -1, 255, 3)
        c = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        mask = np.zeros(mask.shape, dtype="uint8")
        cv2.drawContours(mask, c, -1, 255, thickness=cv2.FILLED)
        mask2 = np.zeros(mask.shape, dtype="uint8")
        cv2.drawContours(mask2, boi, -1, 255, 5)
        mask2 = cv2.bitwise_not(mask2)
        # show(mask2)
        box = cv2.bitwise_and(img, img, mask=mask)
        mask2 = cv2.bitwise_and(box, mask2)
        return mask2

    # -------------Grabs all the option boxes within the answer box------------
    def answerBoxContours(self, box):
        # cv2.imwrite("track.jpeg", box)
        # box = cv2.threshold(box,86, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        box = self.threshed(box, 86)
        # show(box)
        # box_blur = cv2.GaussianBlur(box,(5,5),0)
        # show(box_blur,"blur")
        cnts = cv2.findContours(box.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []
        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour, then use the
            # bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)
            if w * h < 1000:
                questionCnts.append(c)

        c = cv2.findContours(box, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[0]
        rectCon = []
        for i in c:
            (x, y, w, h) = cv2.boundingRect(i)
            if w * h > 0 and w * h < 5000:
                rectCon.append(i)

            # area = cv2.contourArea(i)
            # print(area)
            # if area>100:
            #     rectCon.append(i)
        inside_c = self.crop.copy()

        answermask = np.zeros(inside_c.shape[0:2], dtype="uint8")
        cv2.drawContours(answermask, rectCon, -1, 255, -1)
        # print(len(rectCon))
        # show(answermask, "inside_c"+str(len(c)))
        answermask = cv2.GaussianBlur(answermask, (5, 5), 0)
        mc = cv2.findContours(answermask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        mcf = []
        for i in mc:
            (x, y, w, h) = cv2.boundingRect(i)
            if w * h > 300:
                mcf.append(i)

        return mcf

    # -------------Labels contours on an image-----------------
    def labelImage(self, img, mcf):
        cm = img.copy()
        for (i, c) in enumerate(mcf):
            cm = contours.label_contour(cm, c, i)
        self.show(cm, "CMMM")

    # ----------Retrieves final list of answers------------------
    def getAnswers(self, box, mcf, flag, answerlist):
        count_columns = 0
        highest = 0
        ques_no = 15
        if flag:
            ques_no = 0
        res = np.zeros(box.shape[0:2], dtype="uint8")
        # print("length",len(mcf))
        mcf.sort(key=lambda x: self.getContourPrecedence(x, box.shape[1]))
        # mcf = contours.sort_contours(mcf,method="top-to-bottom")[0]
        self.labelImage(self.crop, mcf)
        for i in range(len(mcf)):
            m = np.zeros(self.crop.shape[0:2], dtype="uint8")
            # print(box.shape)
            cv2.drawContours(m, mcf[i : i + 1], -1, 255, -1)
            # show(m, "BOX"+str(i%10))
            m = cv2.bitwise_and(box, box, mask=m)
            # self.show(m, "BOX" + str(i % 10))
            # show(m, "WHAT")
            # m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
            # show(m, "BOX"+str(count_columns%4))
            total = cv2.countNonZero(m)
            if count_columns % 4 == 0:
                count_columns = 0
                highest = 0
            if total > highest and total > 700:
                # print(total,"x:",mcf[i][0][0])
                # print(ques_no - i // 4, highest, total, count_columns)
                # if(ques_no-i//4==5):
                # self.show(m, str(count_columns))
                highest = total
                answerlist[ques_no + 1 + i // 4] = count_columns  # ,count_columns]
            count_columns += 1
        return answerlist

    def getContourPrecedence(self, contours, cols):
        tolerance_factor = 24
        origin = cv2.boundingRect(contours)
        return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

    def getTextArea(self, img):
        x = img.shape[0]
        y = img.shape[1]
        img = img[0 : int(0.25 * x), 0:y]
        cv2.imwrite("image_processing/test.jpeg", img)
        # self.show(img, "WORKS?")
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thres = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY_INV)[1]
        # self.show(thres, "Thres")
        cnts = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        final_c = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w > 50 and h < 0.1 * img.shape[1]:
                # print(h/img.shape[1])
                final_c.append(c)

        # print(len(final_c))
        # copy = img.copy()
        # cv2.drawContours(copy, final_c, -1, (0,255,0), 2)
        # self.show(copy, "contours")
        # print(self.getText(thres))
        # self.insertionSort(final_c)

        # final_c = contours.sort_contours(final_c, method="top-to-bottom")[0]
        text_inputs = []
        for i in range(len(final_c)):
            mask = np.zeros(thres.shape, dtype="uint8")
            cv2.drawContours(mask, final_c[i : i + 1], -1, 255, -1)
            text_box = cv2.bitwise_and(thres, thres, mask=mask)
            # self.show(text_box, "text"+str(i))
            text_inputs.append(self.getText(text_box))
        self.student_id = text_inputs[2]
        return text_inputs

    def getText(self, img):
        # reader = easyocr.Reader(['en'],gpu = False)
        # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # sharpen = cv2.filter2D(img, -1, sharpen_kernel)
        # thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # r_easy_ocr=reader.readtext(thresh,detail=0)
        # return(r_easy_ocr)
        reader = easyocr.Reader(["en"], gpu=False)  # load once only in memory.
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)[1]
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(img, -1, sharpen_kernel)
        # cv2.imshow("thres", sharpen)
        r_easy_ocr = reader.readtext(img, detail=0)
        return r_easy_ocr

    def getSortedContours(self, cnts):

        pass


if __name__ == ("__main__"):
    x = Sheet("image_processing/sample_sheet#8.jpeg")
    # x = cv2.cvtColor()
    # print(x.answerlist)
    # print(x.getText(x.original))
    print(x.answerlist)
    print(x.text_boxes)
    # cv2.waitKey(0)
