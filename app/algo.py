import requests
import json
from app.form import RiskForm

def getData():
	class State:
		def __init__(self, state, positive, positiveIncrease, inIcuCurrently, hospitalizedCurrently, dataQualityGrade  ):
			self.state = state
			self.positive = positive
			self.positiveIncrease = positiveIncrease
			#self.totalTestResultsIncrease = totalTestResultsIncrease
			self.icuCurrently = inIcuCurrently
			self.hospCurrently = hospitalizedCurrently
			self.stateGrade = dataQualityGrade
	
	# empty dict to hold data returned from api call
	stateList = {}
	stateObject = []

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


	icuCurrently = 0
	hospCurrently = 0
	stateGrade = 'Z'
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
				state = stateList[i].get('state')
				# get the number of total positive cases and daily increase in cases for all states
				if (stateList[i].get('positive') >= 0):
					all_states_pos[count] = stateList[i].get('positive')
					positive = stateList[i].get('positive')
				if (stateList[i].get('positiveIncrease') >= 0):
					all_states_pos_inc[count] = stateList[i].get('positiveIncrease')
					positiveIncrease = stateList[i].get('positiveIncrease')
				
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
				try:
					if icuCurrently == None:
						icuCurrently = 0
					if hospCurrently == None:
						hospCurrently = 0		
				except:
					print("hosp/icu data okay")	
			stateObject.append( State(state, positive, positiveIncrease, icuCurrently, hospCurrently, stateGrade))
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


	labelList = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 
				'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 
				'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 
				'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 
				'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 
				'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 
				'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

	temp_pos = []
	temp_pos_inc = []

	#create list with positive case numbers
	for obj in stateObject:
		temp_pos.append(obj.positive)
		temp_pos_inc.append(obj.positiveIncrease)

	zipped_pos = dict(zip(labelList, temp_pos))
	zipped_pos_inc = dict(zip(labelList, temp_pos_inc))
	#print("zipped", zipped_pos)

	temp_zipped_pos = {}
	temp_zipped_pos_inc = {}

	sorted_pos_total = {}
	sorted_pos_inc = {}

	temp_zipped_pos = sorted(zipped_pos.items(), key=lambda x: x[1], reverse=True)
	temp_zipped_pos_inc = sorted(zipped_pos_inc.items(), key=lambda x: x[1], reverse=True)

	

	for i in temp_zipped_pos:
		#print(i[0], i[1])
		sorted_pos_total[i[0]] = i[1]
	print("sorted_pos_total: ", sorted_pos_total)

	for i in temp_zipped_pos_inc:
		#print(i[0], i[1])
		sorted_pos_inc[i[0]] = i[1]
	print("sorted_pos_inc: ", sorted_pos_inc)
	
	print("sorted_pos_total[user_state]: ", sorted_pos_total[user_state.upper()])

	#@for item in sort_pos_zipped:
		#print(item)
	
	#return risk_rating, state_score, stateList, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, icuCurrently, hospCurrently, index, all_states_pos, all_states_pos_inc, stateGrade
	return risk_rating, state_score, stateList, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, icuCurrently, hospCurrently, index, sorted_pos_total, sorted_pos_inc, stateGrade, all_states_pos, all_states_pos_inc