# import the necessary packages
from imutils.perspective import four_point_transform
import numpy as np
import imutils
import cv2
#"sample_sheet#5A.jpeg"

class Sheet:
	def __init__(self, imgAddress):
		self.original = cv2.imread(imgAddress)
		#self.show(self.original, "huh")
		self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
		edged = cv2.Canny(blurred, 75, 200)
		self.warped = self.warpImage(edged)
		thresh = self.threshed(self.warped, 50)
		questionCnts = self.getBoxContours(thresh)
		self.box_contour_img = self.warped.copy()
		cv2.drawContours(self.box_contour_img, questionCnts,-1,(0,255,0),2)
		self.show(self.box_contour_img, "Box Contours")
		#cv2.imshow("Contours",cv2.resize(cont, None, fx=0.4, fy=0.4))
		#cv2.imwrite("processed_si.jpeg",cont)
		cv2.waitKey(0)
		


	def warpImage(self, img):
		cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
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
				# then we can assume we have found the paper
				if len(approx) == 4:
					docCnt = approx
					break

		# apply a four point perspective transform to both the
		# original image and grayscale image to obtain a top-down
		# birds eye view of the paper
		original = four_point_transform(self.original, docCnt.reshape(4, 2))
		warped = four_point_transform(self.gray, docCnt.reshape(4, 2))
		return warped
	
	def resized(self, img):
		return cv2.resize(img,None,fx=0.4,fy=0.4)

	def show(self,img,x=''):
		cv2.imshow(x, self.resized(img))
	
	def threshed(self, img, val):
		res = cv2.threshold(img, val, 255,             #50
				cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		return res
		

	def getBoxContours(self, img):
		cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		questionCnts = []

		# loop over the contours
		for c in cnts:
			# compute the bounding box of the contour, then use the
			# bounding box to derive the aspect ratio
			(x, y, w, h) = cv2.boundingRect(c)
			ar = w / float(h)

			# in order to label the contour as a question, region
			# should be sufficiently wide, sufficiently tall, and
			# have an aspect ratio approximately equal to 1
			if w >= 20 and h >= 20 and w/h<2:
				questionCnts.append(c)
		return questionCnts



x = Sheet("image_processing\sample_sheet#5A.jpeg")









		
# def prep_image(imgAddress):
# 	image = cv2.imread(imgAddress)
# 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 	edged = cv2.Canny(blurred, 75, 200)

# cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# docCnt = None

# # ensure that at least one contour was found
# if len(cnts) > 0:
# 	# sort the contours according to their size in
# 	# descending order
# 	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# 	# loop over the sorted contours
# 	for c in cnts:
# 		# approximate the contour
# 		peri = cv2.arcLength(c, True)
# 		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

# 		# if our approximated contour has four points,
# 		# then we can assume we have found the paper
# 		if len(approx) == 4:
# 			docCnt = approx
# 			break

# # apply a four point perspective transform to both the
# # original image and grayscale image to obtain a top-down
# # birds eye view of the paper
# paper = four_point_transform(image, docCnt.reshape(4, 2))
# warped = four_point_transform(gray, docCnt.reshape(4, 2))


# # apply Otsu's thresholding method to binarize the warped
# # piece of paper
# thresh = cv2.threshold(warped, 50, 255,
# 	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# cv2.imshow("original", cv2.resize(image, None, fx=0.4, fy=0.4))
# cv2.imshow("warped", cv2.resize(warped,None, fx=0.4, fy=0.4))
# cv2.imshow("thres", cv2.resize(thresh,None, fx=0.4, fy=0.4))




# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# questionCnts = []

# # loop over the contours
# for c in cnts:
# 	# compute the bounding box of the contour, then use the
# 	# bounding box to derive the aspect ratio
# 	(x, y, w, h) = cv2.boundingRect(c)
# 	ar = w / float(h)

# 	# in order to label the contour as a question, region
# 	# should be sufficiently wide, sufficiently tall, and
# 	# have an aspect ratio approximately equal to 1
# 	if w >= 20 and h >= 20 and w/h<2:
# 		questionCnts.append(c)

# cont = warped.copy()
# cv2.drawContours(cont, questionCnts,-1,(0,255,0),2)
# cv2.imshow("Contours",cv2.resize(cont, None, fx=0.4, fy=0.4))
# cv2.imwrite("processed_si.jpeg",cont)
# cv2.waitKey(0)