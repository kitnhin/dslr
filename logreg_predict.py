import sys
import math
import numpy as np
import utils.data_loader as dl
import utils.maths_fts as mf
import utils.numeric_utils as nu

import json

#variables
file_contents = ""
field_values = []
field_names = []
all_student_scores = []

#params
weights = {}
means = []
stds = []

#getting data
def load_params():
	global weights, means, stds
	try:
		with open("params.json") as file:
			model_data = json.load(file)
		
		weights = model_data["weights"]
		means = model_data["means"]
		stds = model_data["stds"]
		return True
	
	except Exception as e:
		print("Unable to open params file (please train model if havent)")
		return False
	

def extract_all_student_data():

	global all_student_scores

	#extract the indexes
	course_indices = [
		field_names.index("Astronomy"), field_names.index("Herbology"), field_names.index("Divination"),
		field_names.index("Muggle Studies"), field_names.index("Ancient Runes"), field_names.index("History of Magic"),
		field_names.index("Transfiguration"), field_names.index("Potions"), field_names.index("Charms"), field_names.index("Flying")
	]
	
	num_students = len(field_values[0])
	
	for i in range(num_students):
		scores = []
		for course_idx in course_indices:
			score = field_values[course_idx][i].strip()
			scores.append(score)
		all_student_scores.append(scores)


#predicting	

def predict_all_students():
	all_student_houses = []
	for i in range(len(all_student_scores)):
		student_scores = extract_student_score(all_student_scores[i])
		predicted_house = predict_house(student_scores)
		all_student_houses.append(predicted_house)
	write_results(all_student_houses)


def extract_student_score(student_data):

	student_score = []
	
	for i in range(len(student_data)):
		score = student_data[i]
		if not score.strip():
			score = means[i]
		else:
			score = float(score)
		student_score.append(score)
	
	return student_score


def predict_house(student_scores):
	houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]

	normalized_scores = normalise_student_score(student_scores)

	max_confidence = 0
	max_house = ""
	for house in houses:
		confidence = calc_confidence(house, normalized_scores)
		if confidence > max_confidence:
			max_confidence = confidence
			max_house = house

	return max_house


def normalise_student_score(score):
	normalized = []
	for i in range(len(score)):
		normalized.append((score[i] - means[i]) / stds[i])
	return normalized

def calc_confidence(house_name, score):
	#z calculation
	z = weights[house_name][0]
	for i in range(len(score)):
		z += weights[house_name][i + 1] * score[i]

	#normalise to probability (sigmoid calculation)
	return 1 / (1 + math.exp(-z))


#output
def write_results(all_student_houses):
	with open("houses.csv", "w") as file:
		file.write("Index,Hogwarts House\n")
		for i in range(len(all_student_houses)):
			file.write(f"{i},{all_student_houses[i]}\n")
	print("Finish writing results to houses.csv")


if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			raise Exception("Invalid number of arguments")
		
		file_contents = dl.readfile(sys.argv[1])
		field_names, field_values = dl.extract_fields(file_contents)
		# print(field_values[:2])
		extract_all_student_data()

		if not load_params():
			exit()

		predict_all_students()

	except Exception as e:
		print("Error: ", e)