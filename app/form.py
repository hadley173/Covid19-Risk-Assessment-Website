from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class RiskForm(FlaskForm):
	
	stateInputStyle={'style': 'max-width:260px;'}
	intInputStyle={'style': 'max-width:80px; margin-left:10px;'}
	intDataVal=[InputRequired(), NumberRange(min=0, max=25)]

	activity1 = IntegerField('Gone grocery shopping', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity2 = IntegerField('Walked, ran, or biked with others', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity3 = IntegerField('Ate at a restaurant (outdoors)', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity4 = IntegerField('Walked in a busy downtown', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity5 = IntegerField('Spent an hour at a playground', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity6 = IntegerField('Sat in a doctor’s waiting room', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity7 = IntegerField('Gone to a library or museum', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity8 = IntegerField('Visited an elderly relative or friend in their home', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity9 = IntegerField('Sent kids to school, camp, or day care', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity10 = IntegerField('Worked in an office building', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity11 = IntegerField('Gone to a hair salon or barbershop', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity12 = IntegerField('Ate at a restaurant (indoors)', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity13 = IntegerField('Attended a wedding or funeral', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity14 = IntegerField('Traveled by plane', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity15 = IntegerField('Played an organized team sport', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity16 = IntegerField('Worked out at a gym', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity17 = IntegerField('Gone to a theater or amusement park', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity18 = IntegerField('Attended an event with 500+ people', default=0, validators=intDataVal, render_kw=intInputStyle)
	activity19 = IntegerField('Gone to a bar', default=0, validators=intDataVal, render_kw=intInputStyle)

	statename = SelectField(
					  	u'Which U.S. state are you in?',
						choices=[
						('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), 
						('CT', 'Connecticut'), ('DC', 'Washington DC'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'), 
						('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisianna'), ('MA', 'Massachusettes'), ('MD', 'Maryland'), ('ME', 'Maine'), 
						('MI', 'Michigan'), ('MN', 'Minnisota'), ('MO', 'Missouri'), ('MP', 'Nortern Mariana Islands'), ('MS', 'Mississippi'), 
						('MT', 'Montana'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NV', 'Nevada'),  
						('NY', 'New York'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'),
						('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'), 
						('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming')],
					  	validators=[InputRequired()], render_kw=stateInputStyle)

	submit = SubmitField('Calculate your risk')