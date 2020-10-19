from flask import render_template, flash, redirect, url_for
from app import app
from app.form import RiskForm
from app.algo import Algo

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/form-input', methods=['GET', 'POST'])
def formInput():
	form = RiskForm()
	if form.validate_on_submit():
		flash('Submission received: {}'.format(form.statename.data))
		algo = Algo()
		algo.state = form.statename.data
		algo.act1 = form.activity1.data
		algo.act2 = form.activity2.data
		algo.act3 = form.activity3.data
		#return redirect(url_for('results')) <-- first attempt, but can't pass in values like this
		return render_template('results.html', title='Risk score', algo=algo)
	return render_template('form-input.html', title = 'Calculator', form=form)

# do we still need this?
#@app.route('/results')
#def results(algo):
#	return render_template('results.html', title='Risk score', algo=algo)

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/activities')
def activities():
	return render_template('activities.html', title='Activities')