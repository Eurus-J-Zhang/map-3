from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session
from flask_migrate import Migrate
from forms import EmotionForm, DemographicInfo, ActionForm
import os
import pymysql
from models import db, Data

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "iloveeurus"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

def handle_form_submission(form, session_key, next_page):
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session[session_key] = data
        return redirect(next_page)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DemographicInfo()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session['index_data'] = data
        session['counter'] = 0
        return redirect(url_for('intro'))
    return render_template('index.html',form=form)

@app.route('/lock_choice', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        slot_choice = request.form.get('slotChoice')
        session['final_choice'] = slot_choice
        if slot_choice == 'A':
            return redirect(url_for('correct'))  # Redirect to the correct page
        elif slot_choice in ('B', 'C'):
            return redirect(url_for('wrong')) # Redirect to the wrong page
        else:
            return render_template('p4.html', error='Please select an option.') 
    return render_template('lock_choice.html')


@app.route('/emo', methods=['GET', 'POST'])
def emo():
    final_choice = session.get('final_choice', None)
    content = {
    'B': {'image_path': 'static/img/ring.jpg'},
    'A_C': {'image_path': 'static/img/alarm.jpg'}
    }
    chosen_content = content['B'] if final_choice == 'B' else content['A_C']
    
    form = EmotionForm()

    result = handle_form_submission(form, 'emo_data', 'end')
    if result:
        index_data = session.get('index_data')
        final_choice = session.get('final_choice')
        emo_data = session.get('emo_data')
        combined_data = {**index_data, 'final_choice': final_choice, **emo_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return result
    return render_template('emo.html',form=form,chosen_content=chosen_content)


# P1
@app.route('/intro')
def intro():
    session['score'] = 30
    return render_template('intro.html')


action_a = 'Take Blue Line to the direction of S14'
action_b = 'Take Blue Line to the direction of S1'
action_c = 'Take Red Line to the direction of S13 '
action_d = 'Take Red Line to the direction of S10 '
action_e = 'Take Yellow Line clockwise '
action_f = 'Take Yellow Line counterclockwise '
message ='+2 mins interruption time'
time_2 = '<br>Time costs: 2 mins'
time_3 = '<br>Time costs: 3 mins'
time_4 = '<br>Time costs: 4 mins'
time_7 = '<br>Time costs: 7 mins'


def get_action_choices(station):
    """Define the action choices and their availability based on the station."""
    if station == 's1':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 's2':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b+time_2, True),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
            ]
    elif station == 's3':
        return [
            ('a', action_a, False),
            ('b', action_b+time_2+ message, True),
            ('c', action_c+time_3+ message, True),
            ('d', action_d+time_3+ message, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 's7':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 's13':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d+time_3, True),
            ('e', action_e+time_7, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 's16':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 's15':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 's6':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 's8':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e+time_4, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 's10':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 's11':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 's12':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 's17':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 's5':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
            ('g', "Get out of the metro", True),
        ]



@app.route('/s1', methods=['GET', 'POST'])
def s1():
    form = ActionForm()
    station = 's1'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            session['score'] -= 2
            return redirect(url_for('s2'))
        elif action == 'e':
            session['score'] -= 7
            return redirect(url_for('s8'))
        elif action == 'f':
            session['score'] -= 7
            return redirect(url_for('s13'))
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices=choices)

# s2
@app.route('/s2', methods=['GET', 'POST'])
def s2():
    form = ActionForm()
    station = 's2'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            session['score'] -= 2
            return redirect(url_for('s3'))
        elif action == 'b':
            session['score'] -= 2
            return redirect(url_for('s1'))

    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s3
@app.route('/s3', methods=['GET', 'POST'])
def s3():
    form = ActionForm()
    station = 's3'
    choices = get_action_choices(station)
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'b':
            session['score'] -= 4
            return redirect(url_for('s2'))
        elif action == 'c':
            session['score'] -= 5
            return redirect(url_for('s7'))
        elif action == 'd':
            session['score'] -= 5
            return redirect(url_for('s6'))

    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s7
@app.route('/s7', methods=['GET', 'POST'])
def s7():
    form = ActionForm()
    station = 's7'
    choices = get_action_choices(station)
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            session['score'] -= 3
            return redirect(url_for('s13'))
        elif action == 'd':
            session['score'] -= 3
            return redirect(url_for('s3'))

    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)


# s13
@app.route('/s13', methods=['GET', 'POST'])
def s13():
    form = ActionForm()
    station = 's13'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'd':
            session['score'] -= 3
            return redirect(url_for('s7'))
        elif action == 'e':
            session['score'] -= 7
            return redirect(url_for('s1'))
        elif action == 'f':
            session['score'] -= 7
            return redirect(url_for('s16'))
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s16
@app.route('/s16', methods=['GET', 'POST'])
def s16():
    form = ActionForm()
    station = 's16'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            session['score'] -= 7
            return redirect(url_for('s13'))
        elif action == 'f':
            session['score'] -= 7
            return redirect(url_for('s15'))

    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s15
@app.route('/s15', methods=['GET', 'POST'])
def s15():
    form = ActionForm()
    station = 's15'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            session['score'] -= 7
            return redirect(url_for('s16'))
        elif action == 'f':
            session['score'] -= 7
            return redirect(url_for('s5'))

    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s6
@app.route('/s6', methods=['GET', 'POST'])
def s6():
    form = ActionForm()
    station = 's6'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            session['score'] -= 3
            return redirect(url_for('s3'))
        elif action == 'd':
            session['score'] -= 3
            return redirect(url_for('s8'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)


# s8
@app.route('/s8', methods=['GET', 'POST'])
def s8():
    form = ActionForm()
    station = 's8'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            session['score'] -= 3
            return redirect(url_for('s6'))
        elif action == 'd':
            session['score'] -= 3
            return redirect(url_for('s10'))
        elif action == 'e':
            session['score'] -= 4
            return redirect(url_for('s11'))
        elif action == 'f':
            session['score'] -= 7
            return redirect(url_for('s1'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)


# s10
@app.route('/s10', methods=['GET', 'POST'])
def s10():
    form = ActionForm()
    station = 's10'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            session['score'] -= 3
            return redirect(url_for('s10'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)


# s11
@app.route('/s11', methods=['GET', 'POST'])
def s11():
    form = ActionForm()
    station = 's11'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            session['score'] -= 4
            return redirect(url_for('s12'))
        elif action == 'f':
            session['score'] -= 4
            return redirect(url_for('s8'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s12
@app.route('/s12', methods=['GET', 'POST'])
def s12():
    form = ActionForm()
    station = 's12'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            session['score'] -= 4
            return redirect(url_for('s17'))
        elif action == 'f':
            session['score'] -= 4
            return redirect(url_for('s11'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)



# s17
@app.route('/s17', methods=['GET', 'POST'])
def s17():
    form = ActionForm()
    station = 's17'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            session['score'] -= 4
            return redirect(url_for('s5'))
        elif action == 'f':
            session['score'] -= 4
            return redirect(url_for('s12'))
        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)

# s5
@app.route('/s5', methods=['GET', 'POST'])
def s5():
    form = ActionForm()
    station = 's5'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    if form.validate_on_submit():
        action = form.action.data
        if action == 'g':
            return redirect(url_for('emo'))        
    return render_template('map.html', form=form, score=session['score'], zip=zip, station=station, choices = choices)



# r_correct
@app.route('/correct')
def correct():
    return render_template('correct.html')

# r_wrong
@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

# end page
@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == "__main__":
    app.run(debug=True)