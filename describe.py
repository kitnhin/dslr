import sys
import math
import numpy as np
import utils.data_loader as dl
import utils.maths_fts as mf
import utils.numeric_utils as nu

#variables
file_contents = ""
field_values = []
field_names = []

def calc_values_and_print():

	#printing settings
	print_field_size = 30
	pad_number = 10

	#print header
	headings = ["field", "count", "mean", "std", "min", "25%", "50%", "75%", "max", "range"]
	for i in range(len(headings)):
		if i == 0:
			print(f"|{headings[i]:^{print_field_size}}|", end = "") # template string (:^ means centre alignment padding, so :^10 means fit element in a 10 space area wif center alighnment)
		else:
			print(f"|{headings[i]:^{pad_number}}|", end = "")
	print(f"\n{(print_field_size + ((pad_number + 1) * len(headings))) * "-"}")

	
	for i in range(1, len(field_values)):
		#print field name
		print(f"|{field_names[i]:<{print_field_size}}|", end="") # :< means left alighnment

		#print number
		if(nu.check_array_is_numeric(field_values[i]) == True):

			#append calculations here and it shall be auto added
			stats_calculated = []
			stats_calculated.append(mf.calc_count(field_values[i]))
			stats_calculated.append(mf.calc_mean(field_values[i]))
			stats_calculated.append(mf.calc_std(field_values[i]))
			stats_calculated.append(mf.calc_min(field_values[i]))
			stats_calculated.append(mf.calc_percentile(field_values[i], 25))
			stats_calculated.append(mf.calc_percentile(field_values[i], 50))
			stats_calculated.append(mf.calc_percentile(field_values[i], 75))
			stats_calculated.append(mf.calc_max(field_values[i]))
			stats_calculated.append(mf.calc_range(field_values[i]))

			for i in range(len(stats_calculated)):
				print(f"|{truncate_number(stats_calculated[i], pad_number):^{pad_number}}|", end="")
			print("")

		else:
			print("| No values for this field")

def truncate_number(number, pad_number):
	rounded = round(number, 2) # limit 2 decimal places
	number_str = str(rounded)
	if len(number_str) > pad_number:
		number_str = number_str[:7] + "..."
	return number_str


if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			raise Exception("Invalid number of arguments")
		
		file_contents = dl.readfile(sys.argv[1])
		field_names, field_values = dl.extract_fields(file_contents)
		calc_values_and_print()

	except Exception as e:
		print("Error: ", e)