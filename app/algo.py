import requests
import json
from app.form import RiskForm

def getData():

	# empty dict to hold data returned from api call
	stateList = {}

	# get state information from api call
	url = 'https://api.covidtracking.com/v1/states/current.json'
	response = requests.get(url)
	json_response = response.json()

	#stateList2 = json_response
	#for item in stateList2.items():
		#print(item)

	# copy api information into dict
	for i in range(56):
		stateList[i] = json_response[i].copy()
		# debug check
		# print(json_response[i])

	form = RiskForm()

	# Pull the user input for state and convert to lower case
	user_state = RiskForm().statename.data.lower()
	print(user_state)

	stateGrade = 'A'
	state_score = 0
	default_risk = 0.083

	
	all_states_pos = {}
	all_states_pos_inc = {}
	index = 0
	count = 0

	# Calc the state multiplier
	try:
		for i in stateList:
			for item in stateList[i].items():
				# get the number of total positive cases and daily increase in cases for all states
				if (stateList[i].get('positive') >= 0):
					all_states_pos[count] = stateList[i].get('positive')
				if (stateList[i].get('positiveIncrease') >= 0):
					all_states_pos_inc[count] = stateList[i].get('positiveIncrease')
				
				# get the data for the specific state chosen by the user
				if(stateList[i].get('state').lower() == user_state):
					index = i
					#print('Match Found: ', stateList[i].get('state').lower())
					#calculate state score 
					try:
						state_score = round(float(stateList[i].get('positiveIncrease') / (stateList[i].get('totalTestResultsIncrease'))), 2)
					except: 
						state_score = 0.083
						print('error getting state score')
					# get hospitilization and ICU data for state chosen by the user	
					icuCurrently = stateList[i].get('inIcuCurrently')
					hospCurrently = stateList[i].get('hospitalizedCurrently')
					stateGrade = stateList[i].get('dataQualityGrade')
			count += 1			
	except ZeroDivisionError:
		state_score = default_risk  #average positive test rate for all states over one week was 8.3%
		print("default state score chosen: ", state_score)


	# need to account for states that do not report this data
	try:
		if icuCurrently == None:
			icuCurrently = 0
		if hospCurrently == None:
			hospCurrently = 0
	except:
		print("no icu and hosp data")
	
	# for debugging
	for item in stateList[index].items():
		print(item)

	# for debugging
	try:
		print('all states pos: ', all_states_pos)
		print('all states pos inc: ', all_states_pos_inc)
		print('all states pos[index]: ', all_states_pos[index])
		print('all states pos inc[index]: ', all_states_pos_inc[index])
	except:
		print("copy error")

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

	# calculate base risk score 
	base_score = 1 - (pow((1 - low_risk_rate), low_risk_events) * pow((1 - mod_risk_rate), mod_risk_events) * pow((1 - mod_high_risk_rate), mod_high_risk_events) * pow((1 - high_risk_rate), high_risk_events))
	

	if base_score == 0:
		base_score = .01 * (1 + state_score)

	# need to account for default state risk with no activities
	# convert risk and state scores to % so they can be displayed to the user
	risk_rating = round(float(base_score *100), 1)
	state_score = round(float(state_score*100), 1)

	
	print("base score: ", base_score)
	
	#if index > 0:
	#	index -= 1
	print("index: ", index)

	
	return risk_rating, state_score, stateList, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, icuCurrently, hospCurrently, index, all_states_pos, all_states_pos_inc, stateGrade

#old version of the algorithm
'''
	# iterate through each state to populate list
	for obj in stateCodes:
		# Build URL query string
		# pull from all states page instead
		
		url = 'https://api.covidtracking.com/v1/states/' + obj + '/current.json'

		#Get response and convert to json payload
		response = requests.get(url)
		json_response = response.json()
		#print(json_response)

		state = json_response['state']
		positive = json_response['positive']
		positive_increase = json_response['positiveIncrease']
		totalTestResultsIncrease = json_response['totalTestResultsIncrease']
		inIcuCurrently = json_response['inIcuCurrently']
		hospitalizedCurrently = json_response['hospitalizedCurrently']

		if inIcuCurrently == None:
			inIcuCurrently = 0
		if hospitalizedCurrently == None:
			hospitalizedCurrently = 0

		# create new object for each state and add to list
		stateList.append( State(state, positive, positive_increase, totalTestResultsIncrease, inIcuCurrently, hospitalizedCurrently))
		
		#DEBUG: Print info
		"""
		print(state)
		print(positive)
		print(positive_increase)
		print(totalTestResultsIncrease)
		print(inIcuCurrently)
		print(hospitalizedCurrently)
		"""

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
				# some of this uneeded
				icuCurrently = i.inIcuCurrently
				hospCurrently = i.hospitalizedCurrently
				print("state score: ", state_score)
				break
	except ZeroDivisionError:
		state_score = default_risk  #average positive test rate for all states over one week was 8.3%
		print("default state score: ", state_score)
		###############################################################################

		###############################################################################
'''

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