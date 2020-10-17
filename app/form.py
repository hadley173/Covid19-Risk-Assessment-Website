from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class RiskForm(FlaskForm):
	states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
						'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
						'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
						'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
						'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

	activity1 = IntegerField('Gone grocery shopping', default=0)
	activity2 = IntegerField('Walked, ran, biked, or sported outdoors with others', default=0)
	activity3 = IntegerField('Ate at a restaurant (outdoors)', default=0)
	statename = SelectField(
					  	'Which U.S. state are you in?',
					  	choices=[(i) for i in states],
					  	validators=[DataRequired()])
	submit = SubmitField('Calculate your risk')