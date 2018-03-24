import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from google import google
import cv2
import os
import glob
import pyscreenshot
import string

def image_to_text(file_name):
	im = Image.open(file_name) # the second one 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1') 
	new_name = "2" + file_name
	im.save(new_name)
	text = pytesseract.image_to_string(Image.open(new_name))
	os.remove(new_name)
	splittext = text.split('\n\n')
	
	content = []
	question = splittext[0]
	content.append(question)
	splittext = splittext[1:]
		
	for curr_content in splittext:
		if '\n' in curr_content:
			new_split = curr_content.split('\n')
			for items in new_split:
				content.append(items)
		else: 
			content.append(curr_content)
	return(content)
		
def calc_levens(result_title, search_str):

	rows = len(result_title) + 1
	cols = len(search_str) + 1
	leven_matr = [[0 for x in range(cols)] for x in range(rows)]
	for i in range (1, rows):
		leven_matr[i][0] = i
	for i in range(1, cols):
		leven_matr[0][i] = i
	for col in range(1, cols):
		for row in range(1, rows):
			if result_title[row-1] == search_str[col-1]:
				cost = 0
			else:
				cost = 1
			leven_matr[row][col] = min(leven_matr[row-1][col] + 1, 
						   leven_matr[row-1][col-1] + cost,
						   leven_matr[row][col-1] + 1)

	return leven_matr[rows-1][cols-1]

def word_freq(result_desc, answer):
	result = result_desc.lower()
	result_spl = result.split()
	return(result_spl.count(answer))
	
file_name = glob.glob('./*.png')[0]
file_name = file_name.split('/')[1]
question_ans = image_to_text(file_name)
quest = question_ans[0]

num_pages = 5
scores = []
answers = question_ans[1:]

for answer in answers: 
	score = 0 
	search_results = google.search(quest)
	for result in search_results:
		answer = answer.lower()
		words = answer.split()
		for word in words:
			curr_score = word_freq(result.description, word)
			score += curr_score
	scores.append(score)

print('\n')
print(scores)
index = scores.index(max(scores)) + 1
answer = question_ans[index]
print("Choose Answer " + str(index) + ": " + answer)
