from flask import render_template, flash, redirect, url_for
from app import app
from app.form import RiskForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/form-input', methods=['GET', 'POST'])
def formInput():
	form = RiskForm()
	if form.validate_on_submit():
		flash('Submission received: {}'.format(form.statename.data))
		return redirect(url_for('results'))
	return render_template('form-input.html', title = 'Calculator', form=form)

@app.route('/results')
def results():
	return render_template('results.html', title='Risk score')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/activities')
def activities():
	return render_template('activities.html', title='Activities')