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
	print(url)

	#Get response and convert to json payload
	response = requests.get(url)
	json_response = response.json()

	print(type(json_response))	# dictionary type
	print(json_response)	# print json

	#iterate through json payload
	for key, value in json_response.items():
		if key == 'state':
			state = value
			print(state)
		if key == 'positiveIncrease':
			positiveIncrease = value
			print(positiveIncrease)
		if key == 'totalTestResultsIncrease':
			totalTestResultsIncrease = value
			print(totalTestResultsIncrease)
	return positiveIncrease
