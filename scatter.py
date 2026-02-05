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

def convert_str_to_float_2arrays(field1, field2):
	#convert str to float
	field1_nums = []
	field2_nums = []
	for i in range(len(field1)):
		if field1[i].strip() != "" and field2[i].strip() != "":  #only extract the values where both fields contain smth
			field1_nums.append(float(field1[i]))
			field2_nums.append(float(field2[i]))
	return field1_nums, field2_nums

def calc_and_display_scatter():

	#find the numberic fields
	numeric_fields_index = nu.find_numeric_fields_idx(field_values)
	
	#calc correlations
	max_corr = 0
	max_corr_idx1 = -1
	max_corr_idx2 = -1
	for i in range(len(numeric_fields_index)):
		for j in range(i + 1, len(numeric_fields_index)):
			field1_idx = numeric_fields_index[i]
			field2_idx = numeric_fields_index[j]
			corr = calc_correlation(field_values[field1_idx], field_values[field2_idx])

			#compare absolute correlations
			if abs(corr) > max_corr:
				max_corr = abs(corr)
				max_corr_idx1 = field1_idx
				max_corr_idx2 = field2_idx
	
	#plot best correlation
	plot_scatter_by_house(field_names[max_corr_idx1], field_names[max_corr_idx2], field_values[max_corr_idx1], field_values[max_corr_idx2], "Best correlation scatterplot")

	#for demo, plot random two fields (shows weak correlation)
	demo_idx1, demo_idx2 = 8, 11
	plot_scatter_by_house(field_names[demo_idx1], field_names[demo_idx2], field_values[demo_idx1], field_values[demo_idx2], "Demo correlation scatterplot")

def plot_scatter_by_house(field1_name, field2_name, field1_values, field2_values, title):
	#Find house index
	house_index = field_names.index("Hogwarts House")

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
		plot.scatter(house_field1[h], house_field2[h], color=colors[h], label=house_names[h])

	plot.xlabel(field1_name)
	plot.ylabel(field2_name)
	plot.title(title)
	plot.legend()
	plot.show()


def calc_correlation(field1, field2):
	#convert str to float
	field1_nums, field2_nums = convert_str_to_float_2arrays(field1, field2)
	
	#convert the fields to number arr
	field1_mean = mf.calc_mean(field1_nums)
	field2_mean = mf.calc_mean(field2_nums)

	#calc numerator
	numerator = 0
	for i in range(len(field1_nums)):
		numerator += (field1_nums[i] - field1_mean) * (field2_nums[i] - field2_mean)
	
	#calc denominator
	sum_partA = 0
	sum_partB = 0
	for i in range(len(field1_nums)):
			sum_partA += (field1_nums[i] - field1_mean)**2
			sum_partB += (field2_nums[i] - field2_mean)**2
	denominator = math.sqrt(sum_partA * sum_partB)

	#combine
	correlation = numerator / denominator
	return correlation


if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			raise Exception("Invalid number of arguments")
		
		file_contents = dl.readfile(sys.argv[1])
		field_names, field_values = dl.extract_fields(file_contents)
		calc_and_display_scatter()

	except Exception as e:
		print("Error: ", e)




#######################################################################################
# Explanation:
# "Similar features" means finding two features that have a strong correlation.

# correlation measures how two variables move together: (values between -1 to 1)
# positive correlation: When one feature increases, the other also tends to increase 
# negative correlation: When one feature increases, the other tends to decrease
# no correlation: The features are independent (no predictable pattern)

# values: 
# 1 = most positive correlation
# 0 = no correlation
# -1 = most negative correlation

# Example: 
# High positive correlation - Students who score high in field1 very likely scores high in field2

# Equation used:

#        Σ[(field1[i] - mean_field1)(field2[i] - mean_field2)]
# r = ------------------------------------------------------
#     √[Σ(field1[i] - mean_field1)²] × √[Σ(field2[i] - mean_field2)²]

# For each data point:
# (field1[i] - mean_field1) = how far X is from its mean
# same for field2
# 
# If student score above average in both fields -> both deviations positive -> product positive
# If students score below average in both fields -> both deviations negative -> product positive
# If student score one field is above average and other below average -> one positive, one negative -> product negative
# Sum all products: large positive = positive correlation, large negative = negative correlation
# But if sum of all products is small, this shows that the products, [(field1[i] - mean_field1)(field2[i] - mean_field2)], cancel out, meaning there's no consistent pattern

#denominator used to normalise results to -1 to 1 range
########################################################################################
