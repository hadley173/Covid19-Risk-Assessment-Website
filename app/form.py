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
						('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), 
						('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), 
						('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), 
						('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), 
						('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')],
					  	validators=[InputRequired()])

	submit = SubmitField('Calculate your risk')