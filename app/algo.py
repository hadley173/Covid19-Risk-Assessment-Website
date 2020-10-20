import requests

def getData():
# TEST: Get current data for California, USA
	api_response = requests.get('https://api.covidtracking.com/v1/states/ca/current.json')
	return api_response.json()['positiveIncrease']

