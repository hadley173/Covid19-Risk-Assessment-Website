import requests
import json
from app.form import RiskForm

class State:
	def __init__(self, state, positive, positiveIncrease, totalTestResultsIncrease, inIcuCurrently, hospitalizedCurrently  ):
		self.state = state
		self.positive = positive
		self.positiveIncrease = positiveIncrease
		self.totalTestResultsIncrease = totalTestResultsIncrease
		self.inIcuCurrently = inIcuCurrently
		self.hospitalizedCurrently = hospitalizedCurrently
		
	# from tutorial i watched, dont think it's needed
	#@classmethod
	#def from_json(cls, json_string):
		#json_dict = json.loads(json_string)
		#return cls(**json_dict)

	#def __repr__(self):
		#return f'<State { self.state }>'

def getData():
	# state codes needed for api call
	stateCodes = ['al', 'ak', 'az','ar','ca','co','ct','dc','de','fl', 'ga','hi','id','il','in','ia',
					'ks','ky','la','me', 'md','ma','mi','mn','ms', 'mo','mt','ne','nv','nh', 'nj','nm',
					'ny','nc','nd','oh','ok','or','pa','ri', 'sc','sd','tn','tx','ut','vt','va','wa','wv','wi','wy']

	# empty list to hold data returned from api call
	stateList = []

	# iterate through each state to populate list
	for obj in stateCodes:
		# Build URL query string
		url = 'https://api.covidtracking.com/v1/states/' + obj + '/current.json'

		#Get response and convert to json payload
		response = requests.get(url)
		json_response = response.json()

		state = json_response['state']
		positive = json_response['positive']
		positive_increase = json_response['positiveIncrease']
		totalTestResultsIncrease = json_response['totalTestResultsIncrease']
		inIcuCurrently = json_response['inIcuCurrently']
		hospitalizedCurrently = json_response['hospitalizedCurrently']

		# create new object for each state and add to list
		stateList.append( State(state, positive, positive_increase, totalTestResultsIncrease, inIcuCurrently, hospitalizedCurrently))
		
		#DEBUG: Print info
		
		print(state)
		print(positive)
		print(positive_increase)
		print(totalTestResultsIncrease)
		print(inIcuCurrently)
		print(hospitalizedCurrently)
		

		#DEBUG: Print json
		#print(json_response)

		# store data
		
		#positive_increase = json_response['positiveIncrease']
		#total_test_results_increase = json_response['totalTestResultsIncrease']
		#icuCurrently = json_response['inIcuCurrently']
		#hospCurrently = json_response['hospitalizedCurrently']
		
		#print(state)
		#print(positive)
		# for bar graph
		###############################################################################

		###############################################################################
	form = RiskForm()

	# Pull the user input for state and convert to lower case
	user_state = RiskForm().statename.data.lower()
	print(user_state)

	state_score = 1
	default_risk = 0.083
	# Calc the state multiplier
	index = 0
	try:
		for i in stateList:
			index += 1
			print(i.state)
			if(i.state.lower() == user_state):
				print("match found")
				state_score = round(float(i.positiveIncrease /i.totalTestResultsIncrease), 2)
				icuCurrently = i.inIcuCurrently
				hospCurrently = i.hospitalizedCurrently
				print("state score: ", state_score)
				break
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
	

	if base_score == 0:
		base_score = .01 * (1 + state_score)

	# need to account for default state risk with no activities
	# convert risk and state scores to % so they can be displayed to the user
	risk_rating = round(float(base_score *100), 1)
	state_score = round(float(state_score*100), 1)

	if(icuCurrently == None): icuCurrently = 0
	if(hospCurrently == None): hospCurrently = 0
	print("base score: ", base_score)
	print('hospCurrently: ', hospCurrently)
	print('icuCurrently: ', icuCurrently)
	index -= 1
	print("index: ", index)

	#return state_score, risk_rating, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, positive, positive_increase, inIcuCurrently, hospitalizedCurrently, totalTestResultsIncrease
	return risk_rating, state_score, stateList, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, user_state, icuCurrently, hospCurrently, index

'''
	def __init__(self, date, state,	dataQualityGrade, death, deathConfirmed, deathIncrease, deathProbable,	
	hospitalized, hospitalizedCumulative, hospitalizedCurrently, hospitalizedIncrease, inIcuCumulative,	
	inIcuCurrently,	negative, negativeIncrease,	negativeTestsAntibody, negativeTestsPeopleAntibody,	
	negativeTestsViral,	onVentilatorCumulative,	onVentilatorCurrently, positive, positiveCasesViral, positiveIncrease,	
	positiveScore, positiveTestsAntibody, positiveTestsAntigen,	positiveTestsPeopleAntibody, positiveTestsPeopleAntigen,	
	positiveTestsViral,	recovered, totalTestEncountersViral, totalTestEncountersViralIncrease, totalTestResults,	
	totalTestResultsIncrease, totalTestsAntibody,	totalTestsAntigen, totalTestsPeopleAntibody, totalTestsPeopleAntigen,	
	totalTestsPeopleViral, totalTestsPeopleViralIncrease, totalTestsViral, totalTestsViralIncrease):
	
		self.date = date
		self.state = state
		self.dataQualityGrade = dataQualityGrade
		self.death = death
		self.deathConfirmed = deathConfirmed
		self.deathIncrease = deathIncrease
		self.deathProbable = deathProbable
		self.hospitalized = hospitalized
		self.hospitalizedCumulative = hospitalizedCumulative
		self.hospitalizedCurrently = hospitalizedCurrently
		self.hospitalizedIncrease = hospitalizedIncrease
		self.inIcuCumulative = inIcuCumulative
		self.inIcuCurrently = inIcuCurrently	
		self.negative = negative
		self.negativeIncrease = negativeIncrease
		self.negativeTestsAntibody = negativeTestsAntibody
		self.negativeTestsPeopleAntibod = negativeTestsPeopleAntibody
		self.negativeTestsViral = negativeTestsViral
		self.onVentilatorCumulative = onVentilatorCumulative
		self.onVentilatorCurrently = onVentilatorCurrently
		self.positive = positive
		self.positiveCasesViral = positiveCasesViral 
		self.positiveIncrease = positiveIncrease	
		self.positiveScore = positiveScore 
		self.positiveTestsAntibody = positiveTestsAntibody
		self.positiveTestsAntigen = positiveTestsAntigen
		self.positiveTestsPeopleAntibody = positiveTestsPeopleAntibody
		self.positiveTestsPeopleAntigen = positiveTestsPeopleAntigen
		self.positiveTestsViral = positiveTestsViral
		self.recovered = recovered
		self.totalTestEncountersViral = totalTestEncountersViral 
		self.totalTestEncountersViralIncrease = totalTestEncountersViralIncrease
		self.totalTestResults = totalTestResults	
		self.totalTestResultsIncrease = totalTestResultsIncrease 
		self.totalTestsAntibody = totalTestsAntibody	
		self.totalTestsAntigen = totalTestsAntigen
		self.totalTestsPeopleAntibody = totalTestsPeopleAntibody
		self.totalTestsPeopleAntigen = totalTestsPeopleAntigen
		self.totalTestsPeopleViral = totalTestsPeopleViral
		self.totalTestsPeopleViralIncrease = totalTestsPeopleViralIncrease
		self.totalTestsViral = totalTestsViral
		self.totalTestsViralIncrease = totalTestsViralIncrease
	
	
	form = RiskForm()

	# Pull the user input for state and convert to lower case
	user_state = RiskForm().statename.data.lower()

	# Build URL query string
	url = 'https://api.covidtracking.com/v1/states/' + state + '/current.json'

	#Get response and convert to json payload
	response = requests.get(url)
	json_response = response.json()

	#DEBUG: Print json
	print(json_response)

	# store data
	state = json_response['state']
	positive_increase = json_response['positiveIncrease']
	total_test_results_increase = json_response['totalTestResultsIncrease']
	icuCurrently = json_response['inIcuCurrently']
	hospCurrently = json_response['hospitalizedCurrently']

	# for bar graph
	###############################################################################
	positive = json_response['positive']
	###############################################################################

	print(state)	
	print("Positive tests: ", positive_increase)	
	print("total tests: " , total_test_results_increase)

'''