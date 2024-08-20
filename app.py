from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session
from flask_migrate import Migrate
from forms import EmotionForm, DemographicInfo, ActionForm
import os
import pymysql
from models import db, Data
from datetime import datetime, timedelta

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
        data.pop('submit', None)
        session['index_data'] = data
        session['counter'] = 0
        return redirect(url_for('intro'))
    return render_template('index.html',form=form)



@app.route('/emo', methods=['GET', 'POST'])
def emo():
    # final_choice = session.get('final_choice', None)
    # content = {
    # 'B': {'image_path': 'static/img/ring.jpg'},
    # 'A_C': {'image_path': 'static/img/alarm.jpg'}
    # }
    # chosen_content = content['B'] if final_choice == 'B' else content['A_C']
    
    form = EmotionForm()

    result = handle_form_submission(form, 'emo_data', 'end')
    if result:
        index_data = session.get('index_data')
        # final_choice = session.get('final_choice')
        emo_data = session.get('emo_data')
        combined_data = {**index_data, **emo_data}
        # combined_data = {**index_data, 'final_choice': final_choice, **emo_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return result
    return render_template('emo.html',form=form)




action_a = 'Take Blue Line to the direction of Perivale'
action_b = 'Take Blue Line to the direction of Windrush Park'
action_c = 'Take Red Line to the direction of Cockfosters '
action_d = 'Take Red Line to the direction of Fayre End '
action_e = 'Take Yellow Line to the direction of Cockfosters'
action_f = 'Take Yellow Line to the direction of Giles Town '
action_g = "Get out of the metro" 
time_2 = '<br>Time costs: 2 mins'
time_3 = '<br>Time costs: 3 mins'
time_4 = '<br>Time costs: 4 mins'
time_7 = '<br>Time costs: 7 mins'


def get_action_choices(station):
    """Define the action choices and their availability based on the station."""
    if station == 'Giles Town':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b+time_2, True),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f, False),
        ]
    elif station == 'Lefting Parkway':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b+time_2, True),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
            ]
    elif station == 'Millstone Square':
        return [
            ('a', action_a, False),
            ('b', action_b+time_2, True),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 'Donningpool North':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 'Cockfosters':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d+time_3, True),
            ('e', action_e,False ),
            ('f', action_f+time_7, True),
        ]
    elif station == 'Oldgate':
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
    elif station == 'Chigwell':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 'Grunham Holt':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d+time_3, True),
            ('e', action_e+time_4, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 'Fayre End':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c+time_3, True),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
        ]
    elif station == 'Tallow Hill':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 'Mudchute':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 'Epping':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_4, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 'Wofford Cross':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b+time_2, True),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 'Conby Vale':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
            ('g', action_g, True),
        ]
    elif station == 'Conby Down':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_4, True),
        ]
    elif station == 'Thornbury Fields':
        return [
            ('a', action_a, False),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e+time_7, True),
            ('f', action_f+time_7, True),
        ]
    elif station == 'Windrush Park':
        return [
            ('a', action_a+time_2, True),
            ('b', action_b, False),
            ('c', action_c, False),
            ('d', action_d, False),
            ('e', action_e, False),
            ('f', action_f, False),
        ]


def process_action(time_cost, redirect_target):
    """Process the action by updating time, score, and redirecting."""
    session['score'] -= time_cost
    current_time_str = session.get('current_time')
    current_time = datetime.strptime(current_time_str, '%H:%M')
    current_time += timedelta(minutes=time_cost)
    session['current_time'] = current_time.strftime('%H:%M')
    return redirect(url_for(redirect_target))

# intro
@app.route('/intro')
def intro():
    session['score'] = 30
    session['current_time'] = '08:30'
    station = 'Giles Town'
    
    form = ActionForm()
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    
    return render_template('intro.html',form=form,zip=zip,station=station, choices=choices)

@app.route('/s1', methods=['GET', 'POST'])
def s1():
    form = ActionForm()
    station = 'Giles Town'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            return process_action(2, 's2')
        elif action == 'b':
            return process_action(2, 's18')
        elif action == 'e':
            return process_action(4, 's19')

    return render_template('map.html', form=form, score=session['score'],current_time=session['current_time'], zip=zip, station=station, choices=choices)

# s2
@app.route('/s2', methods=['GET', 'POST'])
def s2():
    form = ActionForm()
    station = 'Lefting Parkway'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            return process_action(2, 's3')
        elif action == 'b':
            return process_action(2, 's1')

    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'],zip=zip, station=station, choices = choices)

# s3
@app.route('/s3', methods=['GET', 'POST'])
def s3():
    form = ActionForm()
    station = 'Millstone Square'
    choices = get_action_choices(station)
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'b':
            return process_action(2, 's2')
        elif action == 'c':
            return process_action(3, 's7')
        elif action == 'd':
            return process_action(3, 's6')

    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s7
@app.route('/s7', methods=['GET', 'POST'])
def s7():
    form = ActionForm()
    station = 'Donningpool North'
    choices = get_action_choices(station)
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's13')
        elif action == 'd':
            return process_action(3, 's3')

    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s13
@app.route('/s13', methods=['GET', 'POST'])
def s13():
    form = ActionForm()
    station = 'Cockfosters'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'd':
            return process_action(3, 's7')
        elif action == 'f':
            return process_action(7, 's16')
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s16
@app.route('/s16', methods=['GET', 'POST'])
def s16():
    form = ActionForm()
    station = 'Oldgate'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's13')
        elif action == 'f':
            return process_action(7, 's15')

    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s15
@app.route('/s15', methods=['GET', 'POST'])
def s15():
    form = ActionForm()
    station = 'Thornbury Fields'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's16')
        elif action == 'f':
            return process_action(7, 's5')

    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s6
@app.route('/s6', methods=['GET', 'POST'])
def s6():
    form = ActionForm()
    station = 'Chigwell'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's3')
        elif action == 'd':
            return process_action(3, 's8')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s8
@app.route('/s8', methods=['GET', 'POST'])
def s8():
    form = ActionForm()
    station = 'Grunham Holt'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's6')
        elif action == 'd':
            return process_action(3, 's10')
        elif action == 'e':
            return process_action(4, 's11')
        elif action == 'f':
            return process_action(7, 's19')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s10
@app.route('/s10', methods=['GET', 'POST'])
def s10():
    form = ActionForm()
    station = 'Fayre End'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's8')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s11
@app.route('/s11', methods=['GET', 'POST'])
def s11():
    form = ActionForm()
    station = 'Tallow Hill'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's12')
        elif action == 'f':
            return process_action(4, 's8')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s12
@app.route('/s12', methods=['GET', 'POST'])
def s12():
    form = ActionForm()
    station = 'Mudchute'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's17')
        elif action == 'f':
            return process_action(4, 's11')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)



# s17
@app.route('/s17', methods=['GET', 'POST'])
def s17():
    form = ActionForm()
    station = 'Epping'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's5')
        elif action == 'f':
            return process_action(4, 's12')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s4
@app.route('/s4', methods=['GET', 'POST'])
def s4():
    form = ActionForm()
    station = 'Conby Vale'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    if form.validate_on_submit():
        action = form.action.data
        if action == 'g':
            return redirect(url_for('emo'))        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s5
@app.route('/s5', methods=['GET', 'POST'])
def s5():
    form = ActionForm()
    station = 'Wofford Cross'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            return process_action(2, 's14')
        elif action == 'b':
            return process_action(2, 's4')
        elif action == 'e':
            return process_action(7, 's15')
        elif action == 'f':
            return process_action(4, 's17')
  
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s18
@app.route('/s18', methods=['GET', 'POST'])
def s18():
    form = ActionForm()
    station = 'Windrush Park'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            return process_action(2, 's1')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s19
@app.route('/s19', methods=['GET', 'POST'])
def s19():
    form = ActionForm()
    station = 'Conby Down'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's8')
        elif action == 'f':
            return process_action(4, 's1')
        
    return render_template('map.html', form=form, score=session['score'], current_time=session['current_time'], zip=zip, station=station, choices = choices)


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

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    # Only run the development server if the script is executed directly (not via debugger)
    import os
    if os.getenv("FLASK_ENV") != "development":
        app.run(debug=True)