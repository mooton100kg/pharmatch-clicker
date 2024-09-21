import cv2 as cv
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from mss import mss
from PIL import Image
import os

def window_capture():	
	mon = {'top': 0, 'left':0, 'width':1470, 'height':956}

	sct = mss()

	while True:
		sct_img = sct.grab(mon)
		img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
		screenshot = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)

		return screenshot

def openCardImg(image_dir):
	cards = {}
	for filename in os.listdir(image_dir):
		filepath = os.path.join(image_dir, filename)
		if filename.lower().endswith('.png'):
			needle = cv.imread(filepath, cv.IMREAD_UNCHANGED)
			cards[filename.replace('.png','')] = needle
	return cards


def match_single_needle(needle, haystack, threshold, scale_factor):
	needle = cv.resize(needle, (0, 0), fx=scale_factor, fy=scale_factor)
	haystack = cv.resize(haystack, (0, 0), fx=scale_factor, fy=scale_factor)
	result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
	if max_val >= threshold:
		w, h = needle.shape[1], needle.shape[0]
		x = max_loc[0] + int(w / 2)
		y = max_loc[1] + int(h / 2)
		return (x*2, y*2)
	return None

def findNeedleLoc(needles, haystack, threshold):
	needles_loc = {}
	with ThreadPoolExecutor() as executor:
		futures = {executor.submit(match_single_needle, needles[needle], haystack, threshold, 0.5): needle for needle in needles}
		for future in futures:
			needle = futures[future]
			loc = future.result()
			if loc is not None:
				needles_loc[needle] = loc
			if len(needles_loc) >= 5:
				break
	return needles_loc

