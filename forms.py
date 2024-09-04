from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

# Here is for Prolific ID and gender and age
class DemographicInfo(FlaskForm):
    id = StringField('Prolific ID', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('M','Male'),('F','Female'),('O','Others')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=80)])
    submit = SubmitField('Continue', render_kw={'class': 'continue-btn'})

eleven_point_scale = [(str(i), f'Opt{i}') for i in range(11)]

eleven_point_scale_change = [(str(i), f'Opt{i}') for i in range(-5, 6)]

# Here is the first emotion check
class EmotionFormPre(FlaskForm):
    emo1_competence = RadioField('Competence', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_joy = RadioField('Joy', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_pride = RadioField('Pride', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_boredom = RadioField('Boredom', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_irritation = RadioField('Irritation', choices=eleven_point_scale, validators=[DataRequired()]) 
    emo1_anxiety = RadioField('Anxiety', choices=eleven_point_scale, validators=[DataRequired()])  
    emo1_shame = RadioField('Shame', choices=eleven_point_scale, validators=[DataRequired()])  
    
    feedback1 = StringField('',validators=[DataRequired()],widget=TextArea())

class EmotionFormPost(FlaskForm):
    emo2_competence = RadioField('Competence', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_joy = RadioField('Joy', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_pride = RadioField('Pride', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_boredom = RadioField('Boredom', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_irritation = RadioField('Irritation', choices=eleven_point_scale_change, validators=[DataRequired()]) 
    emo2_anxiety = RadioField('Anxiety', choices=eleven_point_scale_change, validators=[DataRequired()])  
    emo2_shame = RadioField('Shame', choices=eleven_point_scale_change, validators=[DataRequired()])  
    
    feedback2 = StringField('',validators=[DataRequired()],widget=TextArea())

class ReflectForm(FlaskForm):
    # strategy_fb = StringField('',validators=[DataRequired()],widget=TextArea())
    reflection = StringField('',validators=[DataRequired()],widget=TextArea())
    # contribution = RadioField('Contribution', choices=[('A','Instructions I was given'),('B','My skill')], validators=[DataRequired()])

class ActionForm(FlaskForm):
    action = RadioField('Choose an action', validators=[DataRequired(message="You must choose an action.")])
    submit = SubmitField('Continue', render_kw={'class': 'continue-btn'})