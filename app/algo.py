import requests
import json
from app.form import RiskForm

def getData():
	class State:
		def __init__(self, state, positive, positive_increase, icu_currently, hospitalized_currently, data_quality_grade  ):
			self.state = state
			self.positive = positive
			self.positive_increase = positive_increase
			self.icu_currently = icu_currently
			self.hosp_currently = hospitalized_currently
			self.state_grade = data_quality_grade
	
	# empty dict to hold data returned from api call
	raw_api_data = {}
	state_list = []

	# get state information from api call
	url = 'https://api.covidtracking.com/v1/states/current.json'
	response = requests.get(url)
	json_response = response.json()

	# copy api information into dict
	for i in range(56):
		raw_api_data[i] = json_response[i].copy()
		# debug check
		# print(json_response[i])

	form = RiskForm()

	# Pull the user input for state and convert to lower case
	user_state = RiskForm().statename.data.lower()
	print(user_state)


	icu_currently = 0
	hosp_currently = 0
	state_grade = 'Z'
	state_score = 0
	default_risk = 0.083

	
	#all_states_pos = {}
	#all_states_pos_inc = {}
	index = 0
	count = 0

	# Calc the state multiplier
	try:
		for i in raw_api_data:
			for item in raw_api_data[i].items():
				state = raw_api_data[i].get('state')
				# get the number of total positive cases and daily increase in cases for all states
				if (raw_api_data[i].get('positive') >= 0):
					positive = raw_api_data[i].get('positive')
				if (raw_api_data[i].get('positiveIncrease') >= 0):
					positive_increase = raw_api_data[i].get('positiveIncrease')	
			# get the data for the specific state chosen by the user
			if(raw_api_data[i].get('state').lower() == user_state):
				index = i # keep track of which state the user chose
				#calculate state score 
				try:
					state_score = round(float(raw_api_data[i].get('positiveIncrease') / (raw_api_data[i].get('totalTestResultsIncrease'))), 2)
				except: 
					# set state score to default rating
					state_score = default_risk
					print('error getting state score')
				# get hospitilization and ICU data for state chosen by the user	
				icu_currently = raw_api_data[i].get('inIcuCurrently')
				hosp_currently = raw_api_data[i].get('hospitalizedCurrently')
				state_grade = raw_api_data[i].get('dataQualityGrade')
				# need to account for states that do not report this data
				try:
					if icu_currently == None:
						icu_currently = 0
					if hosp_currently == None:
						hosp_currently = 0		
				except:
					print("hosp/icu data okay")
			state_list.append( State(state, positive, positive_increase, icu_currently, hosp_currently, state_grade))
			count += 1			
	except ZeroDivisionError:
		state_score = default_risk  #average positive test rate for all states over one week was 8.3%
		print("default state score chosen: ", state_score)
	
	# for debugging
	for item in raw_api_data[index].items():
		print(item)

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

	print("index: ", index)

	temp_pos = []
	temp_pos_inc = []
	label_list = []
	

	#create list with positive case numbers
	for obj in state_list:
		temp_pos.append(obj.positive)
		temp_pos_inc.append(obj.positive_increase)
		label_list.append(obj.state)

	# pair up state codes with positive and positive increase values so they can be sorted later
	zipped_pos_total = dict(zip(label_list, temp_pos))
	zipped_pos_inc = dict(zip(label_list, temp_pos_inc))

	#store necessary information to pass along
	user_state_specifics = {}
	user_state_specifics.update({"state": state_list[index].state})
	user_state_specifics.update({"risk_rating": risk_rating})
	user_state_specifics.update({"state_score": state_score})
	user_state_specifics.update({"state_grade": state_list[index].state_grade})
	user_state_specifics.update({"positive": state_list[index].positive})
	user_state_specifics.update({"positive_increase": state_list[index].positive_increase})
	user_state_specifics.update({"hosp_currently": state_list[index].hosp_currently})
	user_state_specifics.update({"icu_currently": state_list[index].icu_currently})
	user_state_specifics.update({"low_risk_events": low_risk_events})
	user_state_specifics.update({"mod_risk_events": mod_risk_events})
	user_state_specifics.update({"mod_high_risk_events": mod_high_risk_events})
	user_state_specifics.update({"high_risk_events": high_risk_events})
	print(user_state_specifics)


	#return risk_rating, state_score, raw_api_data, low_risk_events, mod_risk_events, mod_high_risk_events, high_risk_events, icu_currently, hosp_currently, index, zipped_pos_total, zipped_pos_inc, state_grade, state_list
	return user_state_specifics, zipped_pos_total, zipped_pos_inc