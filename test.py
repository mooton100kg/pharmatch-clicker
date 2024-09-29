import pyautogui
import time
import cv2 as cv
from pynput import keyboard

from function import *
from variable import *

color = (255,0,255)
run = True
t = time.time()

def on_press(key):
	global run, dropzone_stack

	try:
		if key.char == 'q':
			run = False
			return run
		elif key.char == 'r':
			dropzone_stack = {}
			matchCard = [{},{},{}]
	except AttributeError:
		pass

dropzone = cv.imread('drop.png', cv.IMREAD_GRAYSCALE)
cards_img = openCardImg()
medicine_dict = getCSV()
dropzone_loc = None
cards = [[],[],[],[]]
matchCard = [{},{},{}]
dropzone_stack = {} #{medicine: {'level': 0, 'po':[x,y,w,h], 'cards':[]}}

listener = keyboard.Listener(on_press=on_press)
listener.start()

print(time.time() - t)

#for card in cards_loc:
#	cv.drawMarker(screensho, cards_loc[card], color)

#for (x,y,w,h) in dropzone_loc:
#	top_left = (x,y)
#	bottom_right = (x+w, y+h)
#	cv.rectangle(screenshot, top_left, bottom_right, color)
#	for i in range(3,9,2):
#		xx = int(x + (w*i/8))
#		yy = y + 200
#		cv.drawMarker(screenshot, (xx,yy), color)

while run:
	screenshot = window_capture()
	if dropzone_loc is None or len(dropzone_loc) < 3:
		dropzone_loc = findDropZone(dropzone, screenshot) # [[x,y,w,h]]
	else:
		cards_loc, cards, dropzone_stack = findNeedleLoc(cards_img, screenshot, dropzone_loc, dropzone_stack, cards)
		matchCard = checkCard(cards, medicine_dict, matchCard)
	print(cards)
	if len(cards[0]) > 0:
		dropCard(cards_loc, cards[0], dropzone_stack, 'd', None)
	if len(cards[1]) > 0 and len(matchCard[0]) > 0:
		dropCard(cards_loc, cards[1], dropzone_stack, 'm', matchCard[0])
	if len(cards[2]) > 0 and len(matchCard[1]) > 0:
		dropCard(cards_loc, cards[2], dropzone_stack, 'i', matchCard[1])
	if len(cards[3]) > 0 and len(matchCard[2]) > 0:
		dropCard(cards_loc, cards[3], dropzone_stack, 'a', matchCard[2])


#	if cv.waitKey(1) == ord('q'):
#		cv.destroyAllWindows()
#		break

listener.join()


