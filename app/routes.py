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
		userData.state = form.statename.data
		userData.act1 = form.activity1.data
		userData.act2 = form.activity2.data
		userData.act3 = form.activity3.data
		userData.act4 = form.activity4.data
		userData.act5 = form.activity5.data
		userData.act6 = form.activity6.data
		userData.act7 = form.activity7.data
		userData.act8 = form.activity8.data
		userData.act9 = form.activity9.data
		userData.act10 = form.activity10.data
		userData.act11 = form.activity11.data
		userData.act12 = form.activity12.data
		userData.act13 = form.activity13.data
		userData.act14 = form.activity14.data
		userData.act15 = form.activity15.data
		userData.act16 = form.activity16.data
		userData.act17 = form.activity17.data
		userData.act18 = form.activity18.data
		userData.act19 = form.activity19.data

		print("test user data 19", userData.act19)
		#posIncrease = getData()
		posIncrease, state_score, risk_rating = getData()

		#return redirect(url_for('results')) <-- first attempt, but can't pass in values like this
		return render_template('results.html', title='Risk score', userData=userData, posIncrease=posIncrease, state_score=state_score, risk_rating=risk_rating)
	return render_template('form-input.html', title = 'Calculator', form=form)

# do we still need this?
#@app.route('/results')
#def results(algo):
#	return render_template('results.html', title='Risk score')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/activities')
def activities():
	return render_template('activities.html', title='Activities')
