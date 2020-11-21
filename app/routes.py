from flask import render_template, flash, redirect, url_for, jsonify
from app import app
from app.form import RiskForm
from app.algo import get_data

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/form-input', methods=['GET', 'POST'])
def formInput():
	form = RiskForm()
	if form.validate_on_submit():
		# THIS NO LONGER WORKS SINCE WE'RE NOT PASSING THIS ARRAY
		# input validation for negative numbers
		#for i in range(19):
		#	if activity[i] < 0:
		#		activity[i] = 0


		# get information from api and user to be rendered on results page
		user_state_specifics, zipped_pos_total, zipped_pos_inc = get_data()

		return render_template('results.html', title='Risk score', user_state_specifics=user_state_specifics, 
		zipped_pos_total=zipped_pos_total, zipped_pos_inc=zipped_pos_inc)

	return render_template('form-input.html', title = 'Calculator', form=form)

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/activities')
def activities():
	return render_template('activities.html', title='Activities')