import sys
import math
import numpy as np
import matplotlib.pyplot as plot
import utils.data_loader as dl
import utils.maths_fts as mf
import utils.numeric_utils as nu

#variables
file_contents = ""
field_values = []
field_names = []

def calc_and_display_histogram():

	#find the numberic fields
	numeric_fields_index = nu.find_numeric_fields_idx(field_values)
	
	#init the subplot
	num_of_columns = 5
	num_of_rows = math.ceil(len(numeric_fields_index) / num_of_columns)
	fig, axes = plot.subplots(num_of_rows, num_of_columns, figsize=(15, len(numeric_fields_index)*0.6)) #figsize is the total figure size so idh to always zoom
	axes = axes.flatten() #axes is a 2d array of plot objects, flatten makes it 1D so i can access it easier
	plot.subplots_adjust(hspace=0.5, wspace=0.6) #set spacing between plots

	best_score = 999999999999
	best_course = ""
	best_course_index = 0
	for i in range(len(numeric_fields_index)):
		score = plot_histogram(field_values[numeric_fields_index[i]], field_names[numeric_fields_index[i]], axes[i])
		if score < best_score:
			best_course = field_names[numeric_fields_index[i]]
			best_score = score
			best_course_index = numeric_fields_index[i]
	plot.show()

	fig2, ax2 = plot.subplots(1, 1, figsize=(10, 6))
	plot_histogram(field_values[best_course_index], best_course, ax2)
	ax2.set_title("Best course: " + best_course)
	ax2.legend()
	plot.show()


def plot_histogram(field, fieldname, axes):

	#find house index
	house_index = field_names.index("Hogwarts House")

	# Extract scores
	house_names = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
	colors = ['red', 'green', 'blue', 'yellow']
	house_scores = []
	for i in range(4):
		house_scores.append([])

	for i in range(len(field)):
		if field[i].strip() == "":
			continue
		house = field_values[house_index][i].strip()
		score = float(field[i].strip())
		for h in range(4):
			if house == house_names[h]:
				house_scores[h].append(score)
				break

	#plot for each house
	for h in range(4):
		axes.hist(house_scores[h], alpha=0.5, color=colors[h], label=house_names[h])

	axes.set_xlabel("Scores")
	axes.set_ylabel("Frequency")
	axes.set_title(fieldname)

	# calculate mean to see which course has houses with similar scores
	house_means = []
	for h in range(4):
		mean = mf.calc_mean(house_scores[h])
		house_means.append(mean)

	average_mean = sum(house_means) / 4

	total_difference = 0
	for mean in house_means:
		difference = abs(mean - average_mean)
		total_difference += difference

	score = total_difference / 4
	return score


if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			raise Exception("Invalid number of arguments")
		
		file_contents = dl.readfile(sys.argv[1])
		field_names, field_values = dl.extract_fields(file_contents)
		calc_and_display_histogram()

	except Exception as e:
		print("Error: ", e)