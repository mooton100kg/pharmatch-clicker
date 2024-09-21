import pyautogui
import time
from pynput import keyboard
import os

def findCard(card):
	card = os.path.join(IMAGE_DIR, card)
	try:
		position = pyautogui.locateCenterOnScreen(card, grayscale=True, confidence=0.8)
		return position.x/2,position.y/2
	except pyautogui.ImageNotFoundException:
		return None, None

def findPlay():
	try:
		position = pyautogui.locateCenterOnScreen('drop.png', grayscale=True, confidence=0.8)
		return position.x/2,position.y/2
	except pyautogui.ImageNotFoundException:
		return None, None

def on_press(key):
	try:
		if key.char == 'a':
			for card in CARDS:
				x, y = findCard(card)
				print(x,y, card)
				if x:
					pyautogui.moveTo(x, y)
		if key.char == 's':
			x, y = findPlay()
			print(x,y)
			pyautogui.dragTo(x,y, 2, button='left')
		if key.char == '`':
			print(pyautogui.displayMousePosition())
	except AttributeError:
		pass

	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()
	
