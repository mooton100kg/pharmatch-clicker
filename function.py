import cv2 as cv
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
from mss import mss
from PIL import Image
import os
import pyautogui

from variable import threshold, scale_factor, image_dir, csv_path 

def dropCard(cards_loc, cards, dropzone_stack, t, matchCard):
	if t == 'd':
		i = 3
	elif t == 'm':
		i = 3
	elif t == 'i':
		i = 5
	elif t == 'a':
		i = 7

	for card in cards:
		if t != 'd':
			d = matchCard[card]
		else:
			d = card

		x,y,w,h = dropzone_stack[d]['po']
		xx = int(x + (w*i/8))
		yy = int(y + 200)

		if dropzone_stack[d]['level'] >= 3:
			pyautogui.scroll(1000, xx/2, yy/2)
			

		pyautogui.moveTo(cards_loc[card][0]/2, cards_loc[card][1]/2)
		pyautogui.dragTo(xx/2, yy/2, 0.2, button="left")
		print('move card')

def checkCard(cards, medicine_dict, matchCard):
	d = [card[1:] for card in cards[0]]
	m = [card[1:] for card in cards[1]]
	i = [card[1:] for card in cards[2]]
	a = [card[1:] for card in cards[3]]

	with ThreadPoolExecutor() as executor:
		futures = {executor.submit(checkSingleCard, card_d, m,i,a, medicine_dict): card_d for card_d in d}
		for future in futures:
			card_d = futures[future]
			matchStack = future.result()
			for i in range(3):
				for card in matchStack[i]:
					di = [card] = 'd' + card_d
					matchCard[i].append(di)
	return matchCard


def checkSingleCard(card_d,m,i,a, medicine_dict):
	matchStack = [[],[],[]]
	if card_d in medicine_dict:
		for card_m in m:
			if card_m in medicine_dict[card_d]['mechanism']:
				matchStack[0].append('m' + card_m)
		for card_i in i:
			if card_i in medicine_dict[card_d]['indication']:
				matchStack[1].append('i' + card_i)
		for card_a in a:
			if card_a in medicine_dict[card_d]['adr']:
				matchStack[2].append('a' + card_a)
	else:
		print(card_d)
	return matchStack
			
def getCSV():
	df = pd.read_csv(csv_path)
	medicine_dict = {}
	for index, row in df.iterrows():
		medicine = row['Medicine'].strip().lower()

		indications = [ind.strip().lower() for ind in str(row['Indication']).split('\n') if ind]
		side_effects = [adr.strip().lower() for adr in str(row['ADR']).split('\n') if adr]
		mechanism = row['Mechanism'].strip().lower()

		medicine_dict[medicine] = {
			"indication": indications,
			"mechanism": mechanism,
			"adr": side_effects,
		}

	return medicine_dict


def window_capture():	
	mon = {'top': 0, 'left':0, 'width':1470, 'height':956}

	sct = mss()

	sct_img = sct.grab(mon)
	img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
	screenshot = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

	return screenshot

def openCardImg():
	cards = {}
	for filename in os.listdir(image_dir):
		filepath = os.path.join(image_dir, filename)
		if filename.lower().endswith('.png'):
			needle = cv.imread(filepath, cv.IMREAD_GRAYSCALE)
			cards[filename.replace('.png','')] = needle
	return cards


def match_single_needle(needle, haystack):
	#crop haystack
	w, h = haystack.shape[1], haystack.shape[0]
	haystack = haystack[:h, :w-900]
		

	#resize image
	#needle = cv.resize(needle, (0, 0), fx=scale_factor, fy=scale_factor)
	#haystack = cv.resize(haystack, (0, 0), fx=scale_factor, fy=scale_factor)

	result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
	if result is not None:
		min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
		if max_val >= threshold:
			w, h = needle.shape[1], needle.shape[0]
			x = max_loc[0] + int(w / 2) 
			y = max_loc[1] + int(h / 2)
			
			return (int(x),int(y))
	return None

def findNeedleLoc(needles, haystack, dropzone_loc, dropzone_stack, cards):
	needles_loc = {}
	drug = []
	mechanism = []
	indication = []
	adr = []

	with ThreadPoolExecutor() as executor:
		futures = {executor.submit(match_single_needle, needles[needle], haystack): needle for needle in needles}
		for future in futures:
			needle = futures[future]
			loc = future.result()
			if loc is not None:
				needles_loc[needle] = loc

				if needle.startswith('d') and needle not in dropzone_stack:
					level = len(dropzone_stack)
					if level >= 3:
						position = dropzone_loc[level - 3]
					else:
						position = dropzone_loc[level]
					dropzone_stack[needle] = {
						'level': level, 
						'po': position,
						'cards':[]}
					drug.append(needle)
				elif needle.startswith('m'):
					mechanism.append(needle)
				elif needle.startswith('i'):
					indication.append(needle)
				elif needle.startswith('a'):
					adr.append(needle)

			if len(needles_loc) >= 5:
				break
	cards[0].extend(drug)
	cards[1].extend(mechanism)
	cards[2].extend(indication)
	cards[3].extend(adr)
	return needles_loc, cards, dropzone_stack

def findDropZone(needle, haystack):
	dropZone_loc = []

	#crop haystack
	h = haystack.shape[0]
	w = haystack.shape[1]
	#offset_x = w-900

	#haystack = haystack[:h, w-900:w]
		

	#resize image
	#needle = cv.resize(needle, (0, 0), fx=scale_factor, fy=scale_factor)
	#haystack = cv.resize(haystack, (0, 0), fx=scale_factor, fy=scale_factor)

	result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
	if result is not None:
		locations = np.where(result >= threshold)
		locations = list(zip(*locations[::-1]))
		w, h = needle.shape[1], needle.shape[0]

		for loc in locations:
			x = int(loc[0]) # + offset_x
			y = int(loc[1]) 
			dropZone_loc.append([x, y, w, h])
		
		dropZone_loc, weight = cv.groupRectangles(dropZone_loc, 1, 0.5)

		return dropZone_loc
	return None

