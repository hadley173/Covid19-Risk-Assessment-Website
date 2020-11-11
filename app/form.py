from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired

class RiskForm(FlaskForm):
	
	activity1 = IntegerField('Gone grocery shopping', default=0, validators=[InputRequired()])
	activity2 = IntegerField('Walked, ran, biked, or sported outdoors with others', default=0, validators=[InputRequired()])
	activity3 = IntegerField('Ate at a restaurant (outdoors)', default=0, validators=[InputRequired()])
	activity4 = IntegerField('Walked in a busy downtown', default=0, validators=[InputRequired()])
	activity5 = IntegerField('Spent an hour at a playground', default=0, validators=[InputRequired()])
	activity6 = IntegerField('Sat in a doctor’s waiting room', default=0, validators=[InputRequired()])
	activity7 = IntegerField('Gone to a library or museum', default=0, validators=[InputRequired()])
	activity8 = IntegerField('Visited an elderly relative or friend in their home', default=0, validators=[InputRequired()])
	activity9 = IntegerField('Sent kids to school, camp, or day care', default=0, validators=[InputRequired()])
	activity10 = IntegerField('Worked in an office building', default=0, validators=[InputRequired()])
	activity11 = IntegerField('Gone to a hair salon or barbershop', default=0, validators=[InputRequired()])
	activity12 = IntegerField('Ate at a restaurant (indoors)', default=0, validators=[InputRequired()])
	activity13 = IntegerField('Attended a wedding or funeral', default=0, validators=[InputRequired()])
	activity14 = IntegerField('Traveled by plane', default=0, validators=[InputRequired()])
	activity15 = IntegerField('Played an organized team sport', default=0, validators=[InputRequired()])
	activity16 = IntegerField('Worked out at a gym', default=0, validators=[InputRequired()])
	activity17 = IntegerField('Gone to a theater or amusement park', default=0, validators=[InputRequired()])
	activity18 = IntegerField('Attended an event with 500+ people', default=0, validators=[InputRequired()])
	activity19 = IntegerField('Gone to a bar', default=0, validators=[InputRequired()])

	statename = SelectField(
					  	u'Which U.S. state are you in?',
						choices=[
						('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'Washington DC'), ('DE', 'Delaware'), ('FL', 'Florida'), 
						('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisianna'), ('ME', 'Maine'), 
						('MD', 'Maryland'), ('MA', 'Massachusettes'), ('MI', 'Michigan'), ('MN', 'Minnisota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
						('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), 
						('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')],
					  	validators=[InputRequired()])

	submit = SubmitField('Calculate your risk')