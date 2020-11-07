import requests
from app.form import RiskForm

def getData():
	form = RiskForm()
# TEST: Get current data for California, USA
	#return json_response["state"]

	# Pull the user input for state and convert to lower case
	state = RiskForm().statename.data.lower()
	print(state)

	# Build URL query string
	url = 'https://api.covidtracking.com/v1/states/' + state + '/current.json'

	#Get response and convert to json payload
	response = requests.get(url)
	json_response = response.json()

	#DEBUG: Print json
	print(json_response)


	#iterate through json payload
	#for key, value in json_response.items():
	#	if key == 'state':
	#		state = value
	#	if key == 'positiveIncrease':
	#		positive_increase = value
	#	if key == 'totalTestResultsIncrease':
	#		total_test_results_increase = value

	# let's do this instead of iterating through the entire payload!
	state = json_response['state']
	positive_increase = json_response['positiveIncrease']
	total_test_results_increase = json_response['totalTestResultsIncrease']


	print(state)	
	print("Positive tests: ", positive_increase)	
	print("total tests: " , total_test_results_increase)

	default_risk = 0.083
	# Calc the state multiplier
	try:
		state_score = round(float(positive_increase / total_test_results_increase), 2)
		print("state score: ", state_score)
	except ZeroDivisionError:
		state_score = default_risk  #average positive test rate for all states over one week was 8.3%
		print("default state score: ", state_score)

	if state_score <= 0:
		state_score = default_risk
	
	# state risk score capped at 35%
	if state_score >=0.35:
		state_score = 0.35

	low_risk_rate = .02 * (1 + state_score)
	mod_risk_rate = .04  * (1 + state_score)
	mod_high_risk_rate = .08  * (1 + state_score)
	high_risk_rate = .16  * (1 + state_score)

	low_risk_events = form.activity1.data + form.activity2.data + form.activity3.data + form.activity4.data + form.activity5.data + form.activity6.data + form.activity7.data
	mod_risk_events = form.activity8.data + form.activity9.data + form.activity10.data
	mod_high_risk_events = form.activity11.data + form.activity12.data + form.activity13.data + form.activity14.data + form.activity15.data
	high_risk_events = form.activity16.data + form.activity17.data + form.activity18.data + form.activity19.data

	print("low_risk_events", low_risk_events)
	print("mod_risk_events", mod_risk_events)
	print("mod_high_risk_events", mod_high_risk_events)
	print("high_risk_events", high_risk_events)

	base_score = 1 - (pow((1 - low_risk_rate), low_risk_events) * pow((1 - mod_risk_rate), mod_risk_events) * pow((1 - mod_high_risk_rate), mod_high_risk_events) * pow((1 - high_risk_rate), high_risk_events))
	print("base score: ", base_score)

	if base_score == 0:
		base_score = .01 * (1 + state_score)

	# need to account for default state risk with no activities
	# convert risk and state scores to % so they can be displayed to the user
	risk_rating = round(float(base_score *100), 1)
	state_score = round(float(state_score*100), 1)

	return positive_increase, state_score, risk_rating
