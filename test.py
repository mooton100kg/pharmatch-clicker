import pyautogui
import time
import cv2 as cv

from function import *
from variable import *

card_loc = {}
needles_img = openCardImg()

t = time.time()

screenshot = cv.imread('2.png', cv.IMREAD_UNCHANGED)
screensho = cv.imread('3.png', cv.IMREAD_UNCHANGED)
drop = cv.imread('drop.png', cv.IMREAD_UNCHANGED)
needles_loc = findNeedleLoc(needles_img, screenshot)

print(time.time() - t)

for i in needles_loc:
	cv.drawMarker(screensho, needles_loc[i], (255,0,255))

for (x,y,w,h) in findDropZone(drop, screenshot):
	top_left = (x,y)
	bottom_right = (x+w, y+h)
	cv.rectangle(screensho, top_left, bottom_right, (255,0,255))
	for i in range(3,9,2):
		xx = int(x + (w*i/8))
		yy = y + 200
		cv.drawMarker(screensho, (xx,yy), (255,0,255))

cv.imshow('Computer Vision', screensho)

if cv.waitKey() == ord('q'):
	cv.destroyAllWindows()
	




