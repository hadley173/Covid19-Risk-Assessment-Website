import requests
from app.form import RiskForm

def getData():
# TEST: Get current data for California, USA
	#return json_response["state"]

	# Pull the user input for state and convert to lower case
	state = RiskForm().statename.data.lower()
	print(state)

	# Build URL query string
	url = 'https://api.covidtracking.com/v1/states/' + state + '/current.json'
	#print(url)

	#Get response and convert to json payload
	response = requests.get(url)
	json_response = response.json()

	#DEBUG: Print json
	print(json_response)

	#iterate through json payload
	for key, value in json_response.items():
		if key == 'state':
			state = value
			print(state)
		if key == 'positiveIncrease':
			positive_increase = value
			print(positive_increase)
		if key == 'totalTestResultsIncrease':
			total_test_results_increase = value
			print(total_test_results_increase)

	# Calc the state multiplier
	try:
		state_score = round(float(positive_increase / total_test_results_increase), 2)
		print(state_score)
	except ZeroDivisionError:
		state_score = 0
		print(state_score)

	return positive_increase, state_score
