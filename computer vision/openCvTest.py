#!/usr/bin/env python
import cv2
import numpy as np

im = cv2.imread('confirm.jpg')
gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
#img = cv2.fastNLMeansDenoisingMulti(thresh1, 2, 5, None, 4, 7, 35)
kernel = np.ones((28,28),np.uint8)
erosion = cv2.erode(thresh1,kernel,iterations = 1)
small = cv2.resize(erosion, (0,0), fx=0.1, fy=0.1)
cv2.imshow('confirm',small)
cv2.waitKey()
contours,hierarchy = cv2.findContours(erosion,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(im,contours,-1,(0,255,0),-1)
cv2.drawContours(im,contours,-1,(0,255,0),3)
small = cv2.resize(im, (0,0), fx=0.15, fy=0.15)
cv2.imshow('confirm',small)
cv2.waitKey()

f2 = open("contours.txt","w")
idx =0 
for cnt in contours:
    idx += 1
    x,y,w,h = cv2.boundingRect(cnt)
    f2.write(str(idx)+": "+str(w*h)+"\n")
    if (w*h) > 2000:
		roi=im[y:y+h,x:x+w]
		cv2.imwrite("./tableBlocks/"+str(idx) + '.jpg', roi)
    #cv2.rectangle(im,(x,y),(x+w,y+h),(200,0,0),2)
