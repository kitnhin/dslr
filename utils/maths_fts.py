import math

#str calculation functions
def calc_count(values):
	count = 0
	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		count += 1
	return count

def calc_mean(values):
	sum = 0
	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		sum += float(values[i])
	mean = sum / calc_count(values)
	return mean

def calc_std(values):
	mean = calc_mean(values)
	std = 0
	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		std += (float(values[i]) - mean) ** 2
	
	std = math.sqrt(std / calc_count(values))
	return std

def calc_min(values):
	min_value = 2**63   # 9223372036854775808 (64bit int min cuz python has no min wts)

	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		min_value = min(min_value, float(values[i]))
	
	return min_value

def calc_max(values):
	max_value = -2**63

	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		max_value = max(max_value, float(values[i]))
	
	return max_value

def calc_percentile(values, percentile):

	# convert all values to numbers
	numbers = []
	for i in range(len(values)):
		if isinstance(values[i], str) and values[i].strip() == "":
			continue
		numbers.append(float(values[i]))
		
	# steps:
	# 1) sort numbers
	# 2) find pos (number of elements - 1) * (percentile / 100) (n - 1 to take into account index starts from 0)
	# 3) pos is most likely a float, so need interpolation ( small + (big - small) * fractional part of pos)
	# for step 3: if pos = 3.5, small = numbers[3] and big = numbers[4]

	sorted_numbers = sorted(numbers)
	n = calc_count(values)
	pos = (n - 1) * (percentile / 100)
	lower_index = int(math.floor(pos))
	upper_index = int(math.ceil(pos))
	fraction = pos - lower_index

	#interpolation
	nth_percentile_value = sorted_numbers[lower_index] + fraction * (sorted_numbers[upper_index] - sorted_numbers[lower_index])
		
	return nth_percentile_value

#bonus field
def calc_range(values):
	return calc_max(values) - calc_min(values)


