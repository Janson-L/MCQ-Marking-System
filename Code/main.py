import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
import argparse
import imutils
import cv2
import csv

total_question=10.0

#ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
reader = csv.reader(open('Answer.csv'))
ANSWER_KEY={}
next(reader,None)
for row in reader:
    key=int(row[0])-1
    ANSWER_KEY[key]=row[1]

    if row[1]=='A':
        ANSWER_KEY[key]=0
    elif row[1]=='B':
        ANSWER_KEY[key]=1
    elif row[1]=='C':
        ANSWER_KEY[key]=2
    elif row[1]=='D':
        ANSWER_KEY[key]=3
    elif row[1]=='E':
        ANSWER_KEY[key]=4
        

image = cv2.imread("OmrTest10.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)
docCnt = None
# cv2.drawContours(new_image,cnts, -1, (255, 0, 0), 10)
# cv2.imshow("Marked", new_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

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

# cv2.drawContours(new_image,docCnt, -1, (255, 0, 0), 10)

# cv2.imshow("Marked", new_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# apply a four point perspective transform to both the
# original image and grayscale image to obtain a top-down
# birds eye view of the paper
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

# cv2.imshow("Bird View", paper)
# cv2.imshow("Bird View Grey",warped)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# apply Otsu's thresholding method to binarize the warped piece of paper
thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# cv2.imshow("Thresh",thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
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
	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
		questionCnts.append(c)

# cv2.imshow("Marked", cv2.drawContours(paper.copy(),questionCnts, -1, (255, 0, 0), 3))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# sort the question contours top-to-bottom, then initialize
# the total number of correct answers
questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
correct = 0
#maxTotal=0
paper_mark=paper.copy()
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
        maxTotal=0
        # construct a mask that reveals only the current
        # "bubble" for the question
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        # apply the mask to the thresholded image, then
        # count the number of non-zero pixels in the
        # bubble area
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if(total>maxTotal):
            maxTotal=total

    # if the current total has a larger number of total
    # non-zero pixels, then we are examining the currently
    # bubbled-in answer
        if bubbled is None or total >= bubbled[0]:
            if (maxTotal==total):
                bubbled = (total, j)
            else:
                bubbled=(0,10)    
    # initialize the contour color and the index of the
    # *correct* answer
    color = (0, 0, 255)
    k = ANSWER_KEY[q]
    # check to see if the bubbled answer is correct
    if k == bubbled[1]:
        color = (0, 255, 0)
        correct += 1
    # draw the outline of the correct answer on the test
    cv2.drawContours(paper_mark, [cnts[k]], -1, color, 3)

# cv2.imshow("Marked", paper_mark)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# grab the test taker
paper_final=paper_mark.copy()
score = (correct /total_question) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper_final, "{:.2f}%".format(score), (210, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imwrite('Marked/1.jpg',paper_final)
# cv2.imshow("Original", image)
# cv2.imshow("Exam", paper_final)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
