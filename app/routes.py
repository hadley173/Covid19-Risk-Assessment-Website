from flask import render_template, flash, redirect, url_for
from app import app
from app.form import RiskForm
from app.userData import UserData
from app.algo import getData

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/form-input', methods=['GET', 'POST'])
def formInput():
	form = RiskForm()
	if form.validate_on_submit():
		flash('Submission received: {}'.format(form.statename.data))
		userData = UserData()
		activity = {}
		activity[0] = form.activity1.data # frequency for each activity
		activity[1] = form.activity2.data
		activity[2] = form.activity3.data
		activity[3] = form.activity4.data
		activity[4] = form.activity5.data
		activity[5] = form.activity6.data
		activity[6] = form.activity7.data
		activity[7] = form.activity8.data
		activity[8] = form.activity9.data
		activity[9] = form.activity10.data
		activity[10] = form.activity11.data
		activity[11] = form.activity12.data
		activity[12] = form.activity13.data
		activity[13] = form.activity14.data
		activity[14] = form.activity15.data
		activity[15] = form.activity16.data
		activity[16] = form.activity17.data
		activity[17] = form.activity18.data
		activity[18] = form.activity19.data
		for i in range(19):
			# input validation for negative numbers
			if activity[i] < 0:
				activity[i] = 0
			#fill userData object
			userData.act[i] = activity[i]
		userData.state = form.statename.data
		for i in range(19):
			# test print to make sure data copied correctly
			print("USER DATA ARRAY i:",i, activity[i])
		posIncrease, state_score, risk_rating = getData()
		# CHART.JS example line charttest
		legend = 'Monthly Data'
		labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
		values = [10, 9, 8, 7, 6, 4, 8]
		#return redirect(url_for('results')) <-- first attempt, but can't pass in values like this
		return render_template('results.html', title='Risk score', legend=legend, labels=labels, values=values, userData=userData, posIncrease=posIncrease, state_score=state_score, risk_rating=risk_rating)
	return render_template('form-input.html', title = 'Calculator', form=form)

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/activities')
def activities():
	return render_template('activities.html', title='Activities')