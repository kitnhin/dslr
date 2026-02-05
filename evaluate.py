from sklearn.metrics import accuracy_score
import utils.data_loader as dl

actual_results = []
predicted_results = []

def extract_houses(file_contents):

	try:
		rows = file_contents.split("\n")
		first_row_data = rows[0].split(",")
		house_index = first_row_data.index("Hogwarts House")
		houses = []
		for i in range(1, len(rows)):

			if not rows[i].strip():
				continue

			row_data = rows[i].split(",")
			house = row_data[house_index]
			if not house.strip():
				continue
			houses.append(house.strip())
		return houses

	except Exception as e:
		print(e)
		return ""
	

if __name__ == "__main__":
	actual_file_name = "datasets/dataset_truth.csv"
	predicted_file_name = "houses.csv"

	actual_file_content = dl.readfile(actual_file_name)
	predicted_file_content = dl.readfile(predicted_file_name)

	actual_houses = extract_houses(actual_file_content)
	predicted_houses = extract_houses(predicted_file_content)

	if actual_houses and predicted_houses:
		accuracy = accuracy_score(actual_houses, predicted_houses)
		print("Accuracy: ", accuracy)
	else:
		print("Unable to get certain content")