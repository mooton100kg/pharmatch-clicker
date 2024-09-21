import pyautogui
import time
import cv2 as cv

from function import *


THRESHOLD = 0.8
IMAGE_DIR = 'image'  
NEEDLES_IMG = openCardImg(IMAGE_DIR)
card_loc = {}

t = time.time()
#screenshot = window_capture()
SCREENSHOT = cv.imread('2.png', cv.IMREAD_UNCHANGED)

h = SCREENSHOT.shape[0]
w = SCREENSHOT.shape[1]

loc = findNeedleLoc(NEEDLES_IMG, SCREENSHOT, THRESHOLD)
print(loc)
for i in loc:
	cv.drawMarker(SCREENSHOT, loc[i], (255,0,255))
cv.imshow('Computer Vision', SCREENSHOT)

print(time.time() - t)
if cv.waitKey() == ord('q'):
	cv.destroyAllWindows()
	




