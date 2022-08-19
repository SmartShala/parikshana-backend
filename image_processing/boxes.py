import imutils
from imutils import contours
import cv2
import numpy as np

def resized(img):
    return cv2.resize(img,None,fx=0.4,fy=0.4)

def show(img,x=''):
    cv2.imshow(x, resized(img))

crop_f = 20

img = cv2.imread("processed_si.jpeg")
img = img[crop_f:img.shape[0]-crop_f, crop_f:img.shape[1]-crop_f]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
thres = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)[1]
#show(thres, "thres")

cnts = cv2.findContours(thres,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]
#print(len(cnts))

bigboiboxes = sorted(cnts,key=cv2.contourArea, reverse=True)[0:2]

def answer_boxes(box):
    cv2.imwrite("track.jpeg", box)
    box = cv2.threshold(box,86, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #show(box)
    #box_blur = cv2.GaussianBlur(box,(5,5),0)
    #show(box_blur,"blur")
    cnts = cv2.findContours(box.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # loop over the contours
    for c in cnts:
	# compute the bounding box of the contour, then use the
	# bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        if(w*h<1000):
            questionCnts.append(c)

    c = cv2.findContours(box,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)[0]
    rectCon=[]
    for i in c:
        (x,y,w,h) = cv2.boundingRect(i)
        if w*h>0 and w*h<5000:
            rectCon.append(i)

        # area = cv2.contourArea(i)
        # print(area)
        # if area>100:
        #     rectCon.append(i)
    inside_c = img.copy()

    answermask = np.zeros(inside_c.shape[0:2],dtype='uint8')
    cv2.drawContours(answermask, rectCon,-1,255, -1)
    print(len(rectCon))
    #show(answermask, "inside_c"+str(len(c)))
    answermask=cv2.GaussianBlur(answermask,(5,5),0)
    mc = cv2.findContours(answermask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1 )[0]
    mcf=[]
    for i in mc:
        (x,y,w,h) = cv2.boundingRect(i)
        if(w*h>300):
            mcf.append(i)
    mcs = img.copy()
    cv2.drawContours(mcs, mcf[0:1],-1,(0,255,0), -1)
    #show(mcs, "TF"+str(len(mcf)))
    count_columns=0
    highest=0
    correct_option={}
    ques_no=0
    res = np.zeros(box.shape[0:2], dtype='uint8')
    print("length",len(mcf))
    mcf = contours.sort_contours(mcf,method="top-to-bottom")[0]
    cm = img.copy()
    for(i,c) in enumerate(mcf):
        cm=contours.label_contour(cm, c,i)
    show(cm, "CMMM")
    for i in range(len(mcf)):
        m = np.zeros(img.shape[0:2],dtype='uint8')
        # print(box.shape)
        cv2.drawContours(m, mcf[i:i+1],-1,255, -1)
        # show(m, "BOX"+str(i%10))
        m = cv2.bitwise_and(box,box,mask=m)
        # show(m, "BOX"+str(i%10))
        # show(m, "WHAT")
        #m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
        #show(m, "BOX"+str(count_columns%4))
        total = cv2.countNonZero(m)
        
        if count_columns%4==0:
            count_columns=0
            highest=0
        if total>highest:
            # print(total,"x:",mcf[i][0][0])
            print(15-i//4,highest,total,count_columns)
            if(15-i//4==5):
                show(m, str(count_columns))
            highest=total
            correct_option[15-i//4]=chr(ord('D')-count_columns)# ,count_columns]
        count_columns+=1
        # if not (count_columns%4): count_columns = 0
        # if total>600:
        #     res=cv2.bitwise_or(res, m)
        #print(total)
    print(correct_option)

        


for boi in bigboiboxes:
    mask = np.zeros(gray.shape, dtype='uint8')
    cv2.drawContours(mask,boi ,-1,255,3) 
    c = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros(mask.shape, dtype='uint8')
    cv2.drawContours(mask, c,-1,255,thickness=cv2.FILLED)
    mask2 = np.zeros(mask.shape, dtype='uint8')
    cv2.drawContours(mask2, boi,-1, 255,5)
    mask2 = cv2.bitwise_not(mask2)
    #show(mask2)
    box = cv2.bitwise_and(gray,gray,mask=mask)
    mask2 = cv2.bitwise_and(box, mask2)
    #show(mask2)
    answer_boxes(mask2)


cont = img.copy()
cv2.drawContours(cont,bigboiboxes,-1,(0,255,0),2)
cv2.imshow("Contor", resized(cont))
cv2.waitKey(0)