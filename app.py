from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session
from flask_migrate import Migrate
from forms import EmotionForm, DemographicInfo, ActionForm
import os
import pymysql
from models import db, Data
from datetime import datetime, timedelta
import json

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

# Centralized action definitions
actions = {
    'a': 'Take Blue Line to the direction of Perivale',
    'b': 'Take Blue Line to the direction of Windrush Park',
    'c': 'Take Red Line to the direction of Cockfosters',
    'd': 'Take Red Line to the direction of Fayre End',
    'e': 'Take Yellow Line to the direction of Cockfosters',
    'f': 'Take Yellow Line to the direction of Giles Town',
    'g': "Get out of the metro"
}

# Station-specific configurations
station_config = {
    'Giles Town': {'enabled': {'a': '2', 'b': '2', 'e': '4'}, 'disabled': ['c', 'd', 'f']},
    'Lefting Parkway': {'enabled': {'a': '2', 'b': '2'}, 'disabled': ['c', 'd', 'e', 'f']},
    'Millstone Square': {'enabled': {'b': '2', 'c': '3', 'd': '3'}, 'disabled': ['a', 'e', 'f']},
    'Donningpool North': {'enabled': {'c': '3', 'd': '3'}, 'disabled': ['a', 'b', 'e', 'f']},
    'Cockfosters': {'enabled': {'d': '3', 'f': '7'}, 'disabled': ['a', 'b', 'c', 'e']},
    'Oldgate': {'enabled': {'e': '7', 'f': '7'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Thornbury Fields': {'enabled': {'e': '7', 'f': '7'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Chigwell': {'enabled': {'c': '3', 'd': '3'}, 'disabled': ['a','b', 'e', 'f']},
    'Grunham Holt': {'enabled': {'c': '3', 'd': '3', 'e': '4', 'f': '7'}, 'disabled': ['a', 'b']},
    'Fayre End': {'enabled': {'c': '3'}, 'disabled': ['a', 'b', 'd', 'e', 'f']},
    'Tallow Hill': {'enabled': {'e': '4', 'f': '4'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Mudchute': {'enabled': {'e': '4', 'f': '4'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Epping': {'enabled': {'e': '4', 'f': '4'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Wofford Cross': {'enabled': {'a': '2', 'b': '2', 'e': '7', 'f': '4'}, 'disabled': ['c', 'd']},
    'Conby Vale': {'enabled': {'g': ''}, 'disabled': ['a', 'b', 'c', 'd', 'e', 'f']},
    'Conby Down': {'enabled': {'e': '7', 'f': '4'}, 'disabled': ['a', 'b', 'c', 'd']},
    'Windrush Park': {'enabled': {'a': '2'}, 'disabled': ['b', 'c', 'd', 'e', 'f']}
}

def get_action_choices(station):
    """Return action choices based on the station, preserving the order."""
    config = station_config.get(station, {})
    enabled_actions = config.get('enabled', {})
    disabled_actions = set(config.get('disabled', []))
    
    choices = []

    # Iterate over all possible actions in the predefined order
    for action in actions.keys():
        if action in enabled_actions:
            time = enabled_actions[action]
            time_str = f'<br>Time costs: {time} mins' if time else ''
            choice = (action, actions[action] + time_str, True)
        elif action in disabled_actions:
            choice = (action, actions[action], False)
        else:
            # Handle actions that are neither explicitly enabled nor disabled
            choice = (action, actions[action], False)
        
        choices.append(choice)

    return choices


def process_action(time_cost, redirect_target):
    """Process the action by updating time, and redirecting."""
    current_time_str = session.get('current_time')
    current_time = datetime.strptime(current_time_str, '%H:%M')
    current_time += timedelta(minutes=time_cost)
    session['current_time'] = current_time.strftime('%H:%M')
    return redirect(url_for(redirect_target))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DemographicInfo()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        data.pop('submit', None)
        session['index_data'] = data
        # session['counter'] = 0
        return redirect(url_for('intro'))
    return render_template('index.html',form=form)

@app.route('/emo', methods=['GET', 'POST'])
def emo():
    form = EmotionForm()

    if form.validate_on_submit():
        # Get form data and remove CSRF token
        emo_data = form.data
        emo_data.pop('csrf_token', None)
        
        # Store form data in session
        session['emo_data'] = emo_data
        
        # Retrieve necessary session data
        index_data = session.get('index_data', {})
        station_track = session.get('station_track', [])
        station_track_json = json.dumps(station_track)
        result = session.get('result')

        # Combine all data
        combined_data = {**index_data, 'station_track': station_track_json,'result': result, **emo_data}
        
        # Save combined data to the database
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        
        # Redirect to the next page
        return redirect('end')

    return render_template('emo.html', form=form)

# intro
@app.route('/intro')
def intro():
    session['current_time'] = '08:30'
    station = 'Giles Town'
    session['s3_visited'] = False 
    session['result']=None
    session['station_track'] = [] # Initialize as an empty list
    form = ActionForm()
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    
    return render_template('intro.html',form=form,zip=zip,station=station, choices=choices,current_time=session['current_time'],s3_visited=session['s3_visited'])


@app.route('/s1', methods=['GET', 'POST'])
def s1():
    form = ActionForm()
    station = 'Giles Town'
    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 
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

    return render_template('map.html', form=form ,current_time=session['current_time'], 
                           zip=zip, station=station, choices=choices)

# s2
@app.route('/s2', methods=['GET', 'POST'])
def s2():
    form = ActionForm()
    station = 'Lefting Parkway'

    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
         
        if action == 'a':
            return process_action(2, 's3')
        # debug
        elif action == 'b':
            return process_action(2, 's1')

    return render_template('map.html', form=form , current_time=session['current_time'],
                           zip=zip, station=station, choices = choices)

# s3
@app.route('/s3', methods=['GET', 'POST'])
def s3():
    form = ActionForm()
    station = 'Millstone Square'
    choices = get_action_choices(station)
    session['s3_visited'] = True # Set the flag when s3 is visited
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    

    if form.validate_on_submit():
        session['station_track'].append([station,current_time])  # Append station to the list 
        action = form.action.data
        if action == 'b':
            return process_action(2, 's2')
        elif action == 'c':
            return process_action(3, 's7')
        elif action == 'd':
            return process_action(3, 's6')

    return render_template('map.html', form=form , current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s7
@app.route('/s7', methods=['GET', 'POST'])
def s7():
    form = ActionForm()
    station = 'Donningpool North'
    choices = get_action_choices(station)
    # Set the choices for the action field
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's13')
        elif action == 'd':
            return process_action(3, 's3')

    return render_template('map.html', form=form , current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s13
@app.route('/s13', methods=['GET', 'POST'])
def s13():
    form = ActionForm()
    station = 'Cockfosters'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'd':
            return process_action(3, 's7')
        elif action == 'f':
            return process_action(7, 's16')
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s16
@app.route('/s16', methods=['GET', 'POST'])
def s16():
    form = ActionForm()
    station = 'Oldgate'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's13')
        elif action == 'f':
            return process_action(7, 's15')

    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s15
@app.route('/s15', methods=['GET', 'POST'])
def s15():
    form = ActionForm()
    station = 'Thornbury Fields'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's16')
        elif action == 'f':
            return process_action(7, 's5')

    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s6
@app.route('/s6', methods=['GET', 'POST'])
def s6():
    form = ActionForm()
    station = 'Chigwell'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's3')
        elif action == 'd':
            return process_action(3, 's8')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s8
@app.route('/s8', methods=['GET', 'POST'])
def s8():
    form = ActionForm()
    station = 'Grunham Holt'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

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
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s10
@app.route('/s10', methods=['GET', 'POST'])
def s10():
    form = ActionForm()
    station = 'Fayre End'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'c':
            return process_action(3, 's8')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s11
@app.route('/s11', methods=['GET', 'POST'])
def s11():
    form = ActionForm()
    station = 'Tallow Hill'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's12')
        elif action == 'f':
            return process_action(4, 's8')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s12
@app.route('/s12', methods=['GET', 'POST'])
def s12():
    form = ActionForm()
    station = 'Mudchute'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's17')
        elif action == 'f':
            return process_action(4, 's11')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)



# s17
@app.route('/s17', methods=['GET', 'POST'])
def s17():
    form = ActionForm()
    station = 'Epping'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(4, 's5')
        elif action == 'f':
            return process_action(4, 's12')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s4
@app.route('/s4', methods=['GET', 'POST'])
def s4():
    form = ActionForm()
    station = 'Conby Vale'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]
    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 
    
    if form.validate_on_submit():
        action = form.action.data
        if action == 'g':
            return redirect(url_for('correct'))        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)


# s5
@app.route('/s5', methods=['GET', 'POST'])
def s5():
    form = ActionForm()
    station = 'Wofford Cross'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

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
  
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s18
@app.route('/s18', methods=['GET', 'POST'])
def s18():
    form = ActionForm()
    station = 'Windrush Park'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'a':
            return process_action(2, 's1')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)

# s19
@app.route('/s19', methods=['GET', 'POST'])
def s19():
    form = ActionForm()
    station = 'Conby Down'
    choices = get_action_choices(station)
    form.action.choices = [(value, label) for value, label, is_disabled in choices]

    current_time = session['current_time']
    session['station_track'].append([station,current_time])  # Append station to the list 

    if form.validate_on_submit():
        action = form.action.data
        if action == 'e':
            return process_action(7, 's8')
        elif action == 'f':
            return process_action(4, 's1')
        
    return render_template('map.html', form=form, current_time=session['current_time'], zip=zip, station=station, choices = choices)


# r_correct
@app.route('/correct')
def correct():
    session['result']='success'  # record the result
    return render_template('correct.html')

# r_wrong
@app.route('/wrong')
def wrong():
    session['result']='fail'  
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