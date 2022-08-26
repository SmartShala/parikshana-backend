
import cv2 as cv

max_value = 255
#max_type = 3
max_binary_value = 255
#trackbar_type = 'Type: \n 0: RETR_CCOMP \n 1: RETR_EXTERNAL \n 2: RETR_TREE \n 3: RETR_LIST'
trackbar_value = 'Thresh1'
trackbar_valuem = 'Thresh2'

window_name = 'Threshold Demo'


src=cv.imread("image_processing/test.jpeg")
src = cv.resize(src, None, fx=0.4, fy=0.4)
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)


def Threshold_Demo(val):
    #0: Binary
    #1: Binary Inverted
    #2: Threshold Truncated
    #3: Threshold to Zero
    #4: Threshold to Zero Inverted
    # threshold_type = cv.getTrackbarPos(trackbar_type, window_name)
    # threshold_value = cv.getTrackbarPos(trackbar_value, window_name)
    # _, dst = cv.threshold(src_gray, threshold_value, max_binary_value, threshold_type )
    # cv.imshow(window_name, dst)

    a = cv.getTrackbarPos(trackbar_value, window_name)
    b = cv.getTrackbarPos(trackbar_valuem, window_name)
    box = cv.threshold(src_gray,a, b, cv.THRESH_BINARY_INV)[1]
    cv.imshow(window_name, box)

    #c = cv.findContours(box,cv.RETR_CCOMP,cv.CHAIN_APPROX_NONE)[0]
    # rectCon=[]
    # for i in c:
    #     (x,y,w,h) = cv.boundingRect(i)
    #     if w*h>a and w*h<b:
    #         rectCon.append(i)

        # area = cv2.contourArea(i)
        # print(area)
        # if area>100:
        #     rectCon.append(i)
    #inside_c = src.copy()
    # cv.drawContours(inside_c, rectCon,-1,(0,255,0), 2)
    #cv.imshow(window_name,inside_c)




cv.namedWindow(window_name)
#cv.createTrackbar(trackbar_type, window_name , 3, max_type, Threshold_Demo)
# Create Trackbar to choose Threshold value
cv.createTrackbar(trackbar_value, window_name , 0, max_binary_value, Threshold_Demo)
cv.createTrackbar(trackbar_valuem, window_name , 0, max_binary_value, Threshold_Demo)

# Call the function to initialize
Threshold_Demo(0)
# Wait until user finishes program
cv.waitKey()