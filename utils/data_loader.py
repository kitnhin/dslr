def extract_fields(file_contents):

	field_names = []
	field_values = []

	#extract field names
	lines = file_contents.split('\n')
	field_names = lines[0].split(",")
	number_of_fields = len(field_names)

	#init fields
	for i in range(number_of_fields):
		field_values.append([])

	# extract the rest of the fields
	for i in range(1, len(lines)):
		line_parts = lines[i].split(",")
		if len(line_parts) == number_of_fields:
			for j in range(number_of_fields):
				field_values[j].append(line_parts[j])
	
	return field_names, field_values

def readfile(filename):
	file = open(filename)
	file_contents = file.read()
	file.close()
	return file_contents