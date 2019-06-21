
#Bubble sheet scanner and test grader using OMR, Python and OpenCVPython
# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import pandas as pd
import sys
import os
import random
import pytesseract


'''folder = 'engine/temp'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)'''

# construct the argument parse and parse the arguments
# define the answer key which maps the question number
# to the correct answer

#shutil.rmtree('./temp')
image_path = sys.argv[1]
#keys = pd.read_csv(sys.argv[1]).values
#ANSWER_KEY = {}

'''for data in keys:
	ANSWER_KEY[data[0]]=data[1]'''


image = cv2.imread(image_path)
dim = (540, 750)
img_re= cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("re_img", img_re)
# load the image, convert it to grayscale, blur it
# slightly, then find edges

gray = cv2.cvtColor(img_re, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)




# find contours in the edge map, then initialize
# the contour that corresponds to the document
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None


cv2.drawContours(img_re, cnts, -1, (0,0, 255), 3)
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
paper = four_point_transform(img_re, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))


# apply Otsu's thresholding method to binarize the warped
# piece of paper

thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
	if w >= 22 and h >= 22 and ar >= 0.9 and ar <= 1.1:
		questionCnts.append(c)
cv2.imshow("contours", img_re)
cv2.imshow("edged" , edged)
# sort the question contours top-to-bottom, then initialize
# the total number of correct answers
'''
questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
correct = 0

# each question has 5 possible answers, to loop over the
# question in batches of 5
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
	# sort the contours for the current question from
	# left to right, then initialize the index of the
	# bubbled answer
	cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
	bubbled = None
    	# loop over the sorted contours
	for (j, c) in enumerate(cnts):
		# construct a mask that reveals only the current
		# "bubble" for the question
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
 
		# apply the mask to the thresholded image, then
		# count the number of non-zero pixels in the
		# bubble area
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
 
		# if the current total has a larger number of total
		# non-zero pixels, then we are examining the currently
		# bubbled-in answer
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)
        # initialize the contour color and the index of the
	# *correct* answer
	color = (0, 0, 255)
	#k = ANSWER_KEY[q]
 
	# check to see if the bubbled answer is correct
	#if k == bubbled[1]:
	#	color = (0, 255, 0)
	#	correct += 1
 
	# draw the outline of the correct answer on the test
	cv2.drawContours(paper, cnts, -1, color, 3)
    # grab the test taker'''
'''score = (correct / 5.0) * 100

if(score < 40):
	print("Congrats! you have sucessfully failed in the exam: {:.2f}%".format(score))
else:
	print("Sorry to say, you have passed in the exam: {:.2f}%".format(score))

cv2.putText(paper, "{:.2f}%".format(score), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

#storing the result image in temp directory
path ="engine/temp/result"+str(random.randint(1,100))+".jpg"
print(path)
cv2.imwrite(path,paper)'''
cv2.waitKey(0)