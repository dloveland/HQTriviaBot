import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from google import google
import cv2
import os
import glob
import pyscreenshot

def image_to_text(file_name):
	im = Image.open(file_name) # the second one 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1') 
	new_name = "2" + file_name
	im.save(new_name)
	text = pytesseract.image_to_string(Image.open(new_name))
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

	return leven_matr[row][col]
		
file_name = glob.glob('./*.png')[0]
file_name = file_name.split('/')[1]
question_ans = image_to_text(file_name)
searches = []
searches.append(question_ans[0] + ' ' + question_ans[1])
searches.append(question_ans[0] + ' ' + question_ans[2])
searches.append(question_ans[0] + ' ' + question_ans[3])

num_pages = 1
scores = []

for search in searches:
	score = 0 
	counter = 0
	query = search
	search_results = google.search(query)
	for result in search_results:
		curr_score = calc_levens(result.name, search)
		score += curr_score
		counter += 1
	scores.append(score/float(counter))

index = scores.index(min(scores)) + 1
answer = question_ans[index]
print(scores)
print("Choose Answer " + str(index) + ": " + answer)
