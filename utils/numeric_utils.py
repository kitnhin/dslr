def is_numeric(str):
	try:
		float(str.strip())
		return True
	except:
		return False
	
def check_array_is_numeric(arr):
	found_value = False
	for i in range(len(arr)):

		if arr[i].strip() == "":
			continue

		found_value = True

		if is_numeric(arr[i]) == False:
			return False
	
	return found_value # if all are empty strings then auto will return false

def find_numeric_fields_idx(field_values):
	numeric_fields_index = []
	for i in range(1, len(field_values)):
		if(check_array_is_numeric(field_values[i]) == True):
			numeric_fields_index.append(i)
	return numeric_fields_index
