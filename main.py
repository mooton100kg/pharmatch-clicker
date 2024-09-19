import pyautogui
from pynput import keyboard
from time import sleep

card_1 = 213
card_2 = 381
card_3 = 553
card_4 = 727
card_5 = 889
card_y = 463
drug_1 = 1079
drug_2 = 1162
drug_3 = 1244
drug_4 = 1329
cancel = 1226, 807
line_1 = 376
line_2 = 667
line_3 = 771

on = True

def macro(t):
	x, y = pyautogui.position()
	global on
	if t == 'a':
		pyautogui.moveTo(card_3, y)  # Move to start position
	elif t == 's':
		pyautogui.moveTo(drug_2, y)  # Move to start position
	elif t == 'd':
		pyautogui.click(cancel)
		pyautogui.moveTo(x,y)
	elif t == '`':
		on = not on
	print(on)

def on_press(key):
	try:
		if key.char == 'a' and on:
			macro('a')
		elif key.char == 's' and on:
			macro('s')
		elif key.char == 'd' and on:
			macro('d')
		elif key.char == '`':
			macro('`')
	except AttributeError:
		pass  # Handle special keys (like Shift, Ctrl, etc.) that don't have 'char'

with keyboard.Listener(on_press=on_press) as listener:
	listener.join()  # Keep the program running to listen for key presses
