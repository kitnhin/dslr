import sys
import math
import utils.data_loader as dl
import utils.maths_fts as mf
import argparse
import matplotlib.pyplot as plt

import json

#variables
file_contents = ""
field_values = []
field_names = []
costs = {}
learning_rate = 0

#student variables
student_houses = []
student_scores = [] #courses: Astro, Herb, Divination, Muggle, AncientR, History, Trans, Potions, Charms, Flying

#weights
weights = {}
weights["Gryffindor"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
weights["Slytherin"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
weights["Ravenclaw"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
weights["Hufflepuff"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#getting data
def extract_student_data():
	global student_houses, student_scores

	#extract the indexes
	house_index = field_names.index("Hogwarts House")
	course_indices = [
		field_names.index("Astronomy"), field_names.index("Herbology"), field_names.index("Divination"),
		field_names.index("Muggle Studies"), field_names.index("Ancient Runes"), field_names.index("History of Magic"),
		field_names.index("Transfiguration"), field_names.index("Potions"), field_names.index("Charms"), field_names.index("Flying")
	]
	
	num_students = len(field_values[0])
	
	for i in range(num_students):
		house = field_values[house_index][i].strip()

		scores = []
		skip_student = False
		
		for course_idx in course_indices:
			score = field_values[course_idx][i].strip()
			if not score or not house:
				skip_student = True
				break
			scores.append(float(score))
		
		if not skip_student:
			student_houses.append(house)
			student_scores.append(scores)

def normalise_student_score():
	means = []
	stds = []
	num_features = len(student_scores[0])
	num_students = len(student_scores)

	#extract scores for each feature
	for feature_idx in range(num_features):
		feature_values = []
		for student in range(num_students):
			feature_values.append(student_scores[student][feature_idx])
		
		means.append(mf.calc_mean(feature_values))
		stds.append(mf.calc_std(feature_values))
	
	#normalise student scores 
	#equation: (original - mean) / std
	for student_idx in range(num_students):
		for feature_idx in range(num_features):
			original_value = student_scores[student_idx][feature_idx]
			normalised_value = (original_value - means[feature_idx]) / stds[feature_idx]
			student_scores[student_idx][feature_idx] = normalised_value

	return means, stds

def init_batchsize_and_learning_rate(gradient_descend):
	match gradient_descend:
		case "batch" :
			return len(student_scores), 0.1
		case "sgd":
			return 1, 0.0001
		case "minibatch":
			return 30, 0.003
		case _: #default
			return len(student_scores), 0.1


#calculations
def calc_confidence(house_name, score):
	#z calculation
	z = weights[house_name][0]
	for i in range(len(score)):
		z += weights[house_name][i + 1] * score[i]

	#normalise to probability (sigmoid calculation, g)
	return 1 / (1 + math.exp(-z))

def calc_cost(house_name):
	num_of_students = len(student_scores)

	total_cost = 0
	for i in range(num_of_students):
		y_term = 1 if student_houses[i] == house_name else 0
		total_cost += y_term * math.log(calc_confidence(house_name, student_scores[i])) 
		+ (1 - y_term) * math.log(1 - calc_confidence(house_name, student_scores[i]))

	average_cost = -(1/num_of_students) * total_cost
	costs[house_name].append(average_cost)
	return average_cost

def calc_gradient(house_name, batch_size):
	num_weights = len(weights[house_name])
	num_students = len(student_scores)
	gradients = [0] * num_weights
	batch_count = 0
	#calculate the sum part
	for i in range(num_students):
		h = calc_confidence(house_name, student_scores[i])
		y = 1 if student_houses[i] == house_name else 0
		
		gradients[0] += h - y #bias

		for j in range(1, num_weights):
			gradients[j] += (h - y)*student_scores[i][j - 1] #student score need j - 1 cuz the first score (astronomy), is for the second weight
			#above gradient equation is already given in pdf
		
		batch_count += 1

		#update weights after processing batch
		if batch_count == batch_size or i == num_students - 1:

			for k in range(num_weights):
				gradients[k] = gradients[k] / batch_count
			
			update_weights(house_name, gradients)
			
			#reset
			gradients = [0] * num_weights
			batch_count = 0

def update_weights(house_name, gradients):
	global learning_rate
	for i in range(len(weights[house_name])):
		weights[house_name][i] -= learning_rate * gradients[i]

#training loops
def train_house(house_name, iterations, batch_size):
	costs[house_name] = []
	for iteration in range(iterations):
		calc_gradient(house_name, batch_size)
		calc_cost(house_name)

	final_cost = calc_cost(house_name)
	print(f"House training complete: {house_name} - Final cost: {final_cost}")

def train(batch_size):
	iterations = 100 #change later if want
	houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
	print("Starting Training...")
	for house in houses:
		train_house(house, iterations, batch_size)

#output
def save_model(weights, means, stds):
	filename = "params.json"
	data = {
		"weights": weights,
		"means": means,
		"stds": stds
	}
	try:
		f = open(filename, "w")
		f.write(json.dumps(data))
		f.close()
	except Exception:
		print("Failed to save params")
		
def plot_training_costs():
	plt.figure(figsize=(12, 8))
	
	for house in costs:
		plt.plot(costs[house], label=house)
	
	plt.xlabel('Iteration')
	plt.ylabel('Cost (Error)')
	plt.title('Training Cost per House')
	plt.legend()
	plt.grid(True)
	plt.show()

if __name__ == "__main__":
	try:
		
		#parse args
		parser = argparse.ArgumentParser()
		parser.add_argument("--trainDataset", default="datasets/dataset_train.csv")
		parser.add_argument("--gradientDescend", default="batch")
		trainfile = parser.parse_args().trainDataset
		gradient_descend = parser.parse_args().gradientDescend

		
		#processing
		file_contents = dl.readfile(trainfile)
		field_names, field_values = dl.extract_fields(file_contents)
		extract_student_data()
		means, stds = normalise_student_score()
		batch_size, learning_rate = init_batchsize_and_learning_rate(gradient_descend)

		#training
		train(batch_size)
		save_model(weights, means, stds)
		plot_training_costs()

		
	except Exception as e:
		print("Error: ", e)