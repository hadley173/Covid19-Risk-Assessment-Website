import requests
import json
from app.form import RiskForm

def call_api():
	raw_api_data = {}

	# get state information from api call
	url = 'https://api.covidtracking.com/v1/states/current.json'
	response = requests.get(url)
	json_response = response.json()

	# copy api information into dict
	for i in range(56):
		raw_api_data[i] = json_response[i].copy()
	return raw_api_data

# calculate the risk of the user's chosen state and store needed data from the api call
def calc_state_score(raw_api_data, user_state):
	class State:
		def __init__(self, state_code, state_name, positive, positive_increase, icu_currently, hospitalized_currently, data_quality_grade  ):
			self.state_code = state_code
			self.state_name = state_name
			self.positive = positive
			self.positive_increase = positive_increase
			self.icu_currently = icu_currently
			self.hosp_currently = hospitalized_currently
			self.state_grade = data_quality_grade
	state_list = []
	label_dict = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado',
		'CT': 'Connecticut', 'DC': 'Washington DC', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
		'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisianna', 'MA': 'Massachusettes', 'MD': 'Maryland', 'ME': 'Maine',
		'MI': 'Michigan', 'MN': 'Minnisota', 'MO': 'Missouri', 'MP': 'Nortern Mariana Islands', 'MS': 'Mississippi',
		'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',
		'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
		'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
		'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

	icu_currently = 0
	hosp_currently = 0
	state_grade = 'Z'
	state_score = 0
	default_risk = 0.083
	index = 0
	count = 0

	# Calc the state multiplier
	try:
		for i in raw_api_data:
			state_code = raw_api_data[i].get('state')
			state_name = label_dict[state_code]
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
			# populate list with State class object 
			state_list.append( State(state_code, state_name, positive, positive_increase, icu_currently, hosp_currently, state_grade))
			count += 1
	except ZeroDivisionError:
		state_score = default_risk  #average positive test rate for all states over one week was 8.3%
		print("default state score chosen: ", state_score)

	# input validation needed for state misreporting
	if state_score <= 0:
		state_score = default_risk
	
	# state risk score capped at 35%, needed for state misreporting
	if state_score >=0.35:
		state_score = 0.35
	return state_score, state_list, index

def calc_risk_score(state_score, user_state_specifics):
	# get data from user form input
	form = RiskForm()
	risk_rating = 0

	low_risk_rate = .02 * (1 + state_score)
	mod_risk_rate = .04  * (1 + state_score)
	mod_high_risk_rate = .08  * (1 + state_score)
	high_risk_rate = .16  * (1 + state_score)

	low_risk_events = form.activity1.data + form.activity2.data + form.activity3.data + form.activity4.data + form.activity5.data + form.activity6.data + form.activity7.data
	mod_risk_events = form.activity8.data + form.activity9.data + form.activity10.data
	mod_high_risk_events = form.activity11.data + form.activity12.data + form.activity13.data + form.activity14.data + form.activity15.data
	high_risk_events = form.activity16.data + form.activity17.data + form.activity18.data + form.activity19.data

	# calculate base risk score 
	base_score = 1 - (pow((1 - low_risk_rate), low_risk_events) * pow((1 - mod_risk_rate), mod_risk_events) * pow((1 - mod_high_risk_rate), mod_high_risk_events) * pow((1 - high_risk_rate), high_risk_events))

	# need to account for default state risk with no activities
	if base_score == 0:
		base_score = .01 * (1 + state_score)

	# convert risk and state scores to % so they can be displayed to the user
	risk_rating = round(float(base_score*100), 1)
	state_score = round(float(state_score*100), 1)

	# populate dict with data for the user's chosen state
	user_state_specifics.update({"risk_rating": risk_rating})
	user_state_specifics.update({"state_score": state_score})
	user_state_specifics.update({"low_risk_events": low_risk_events})
	user_state_specifics.update({"mod_risk_events": mod_risk_events})
	user_state_specifics.update({"mod_high_risk_events": mod_high_risk_events})
	user_state_specifics.update({"high_risk_events": high_risk_events})

# formatting data before it is passed along to be displayed to the user
def prepare_data(state_list, user_state_specifics, index):
	temp_pos = []
	temp_pos_inc = []
	label_list = []


	#create list with positive case numbers
	for obj in state_list:
		temp_pos.append(obj.positive)
		temp_pos_inc.append(obj.positive_increase)
		label_list.append(obj.state_code)

	# pair up 2 letter state codes with total and daily case numbers so they can be sorted later
	zipped_pos_total = dict(zip(label_list, temp_pos))
	zipped_pos_inc = dict(zip(label_list, temp_pos_inc))

	# populate dict with data for the user's chosen state
	user_state_specifics.update({"state_name": state_list[index].state_name})
	user_state_specifics.update({"state_code": state_list[index].state_code})
	user_state_specifics.update({"state_grade": state_list[index].state_grade})
	user_state_specifics.update({"positive": state_list[index].positive})
	user_state_specifics.update({"positive_increase": state_list[index].positive_increase})
	user_state_specifics.update({"hosp_currently": state_list[index].hosp_currently})
	user_state_specifics.update({"icu_currently": state_list[index].icu_currently})

	return zipped_pos_total, zipped_pos_inc

def get_data():
	# get the state chosen by the user
	user_state = RiskForm().statename.data.lower()

	# empty dict for holding data for the user's chosen state
	user_state_specifics = {}

	# get the data from the api - 'https://api.covidtracking.com/v1/states/current.json'
	raw_api_data = call_api()

	# the state chosen by the user is assigned a risk score
	state_score, state_list, index = calc_state_score(raw_api_data, user_state)

	# the user is given a risk rating based on their activites and state
	calc_risk_score(state_score, user_state_specifics)

	# store necessary information to pass along for display
	zipped_pos_total, zipped_pos_inc = prepare_data(state_list, user_state_specifics, index)

	# send back data when called from routes.py
	return user_state_specifics, zipped_pos_total, zipped_pos_inc