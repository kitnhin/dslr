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

def plot_pair_plot():
	#find numeric fields
	numeric_fields_index = nu.find_numeric_fields_idx(field_values)
	
	num_of_features = len(numeric_fields_index)
	
	#subplot
	fig, axes = plot.subplots(num_of_features, num_of_features, figsize=(15, 15))
	
	#double while loop to loop thru every single combination
	for row in range(num_of_features):
		for col in range(num_of_features):
			field1_idx = numeric_fields_index[row]
			field2_idx = numeric_fields_index[col]
			
			if row == col: #diagonal - plot histogram
				plot_histogram_in_subplot(field_values[field1_idx], axes[row][col])
			else:
				plot_scatter_in_subplot(field_values[field1_idx], field_values[field2_idx], axes[row][col])
			
			#rm axis numbers to save space
			axes[row][col].set_xticks([])
			axes[row][col].set_yticks([])
			
			#label subject on left and bottom edges
			if col == 0: #on the left
				axes[row][col].set_ylabel(field_names[numeric_fields_index[row]], fontsize=5)
			if row == num_of_features - 1: #bottom
				axes[row][col].set_xlabel(field_names[numeric_fields_index[col]], fontsize=5)
	axes[0][0].legend(fontsize=5, bbox_to_anchor=(0, 2)) #bbox specifies where i put my legend box relative to the figure i specify (in this case the top right fig), coords (horizontal, vertical)
	plot.show()

def plot_histogram_in_subplot(field, axes):

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

def plot_scatter_in_subplot(field1_values, field2_values, axes):
	#Find house index
	house_index = -1
	for i in range(len(field_names)):
		if field_names[i].lower() == "hogwarts house":
			house_index = i
			break

	# Extract scores
	house_names = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
	colors = ['red', 'green', 'blue', 'yellow']

	#create 4 arrays, one for each house, then split the field1 and field2 values by each house
	house_field1 = []
	house_field2 = []
	for h in range(4):
		house_field1.append([])
		house_field2.append([])

	# Extract data for each house
	for i in range(len(field1_values)):
		if field1_values[i].strip() == "" or field2_values[i].strip() == "":
			continue

		house = field_values[house_index][i].strip()

		for h in range(4):
			if house == house_names[h]:
				house_field1[h].append(float(field1_values[i].strip()))
				house_field2[h].append(float(field2_values[i].strip()))
				break

	# Plot for each house
	for h in range(4):
		axes.scatter(house_field1[h], house_field2[h], color=colors[h], label=house_names[h], s=1) #s controls the size

if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			raise Exception("Invalid number of arguments")
		
		file_contents = dl.readfile(sys.argv[1])
		field_names, field_values = dl.extract_fields(file_contents)
		plot_pair_plot()

	except Exception as e:
		print("Error: ", e)