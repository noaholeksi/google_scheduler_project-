import os  # Add this line
from flask import Flask, g, jsonify, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restx import Resource, Api, Namespace
from flask_cors import CORS
from scheduler_orm import Activity
import event_scheduler
from schedule_creation import Scheduler
import datetime as dt

from util import get_config

# Ensure FLASK_ENV is set to 'dev_lite'
os.environ['FLASK_ENV'] = 'dev_lite'  # Add this line

app = Flask(__name__)

# Retrieve the environment variable with a default value
flask_env = os.getenv('FLASK_ENV', 'dev_lite')

# Set the environment variable in app.config manually
app.config['ENV'] = flask_env

# Now update the config using the environment variable
app.config.update(get_config(app.config['ENV'], app.open_resource('config.yaml')))

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the Flask-Restx Api
api = Api(app, prefix="/api", doc='/api/docs')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# Define a namespace for schedulers
scheduler_ns = Namespace('schedulers', description='Creating and planning schedulers')
api.add_namespace(scheduler_ns)


    
# # Create a global session for database connections before request
@app.before_request
def init_db():
    if not hasattr(g, 'activities_db'):
        db_engine = create_engine(app.config['DB_ACTIVITIES'])
        g.activities_db = sessionmaker(bind=db_engine)()  # Create a session and store it in `g`

@app.teardown_request
def close_db(exception):
    if hasattr(g, 'activities_db'):
        g.activities_db.close()  # Close the session
        g.pop('activities_db', None)  # Remove the session from `g`


@scheduler_ns.route('/myActivities')
class Activities(Resource):
    def get(self):
        try:
            # Test data to return
            self.clear_expired()
            activities = g.activities_db.query(Activity).all()
            
            # Convert the activities to a list of dictionaries
            activities_list = [{'id': activity.activity_id,'name': activity.name, 'type': activity.type, 'week_days': activity.week_days or "", 'time_pairs':activity.time_pairs or "", "start": activity.start or "", "end": activity.end or "", "also_accomplishes": activity.also_accomplishes or "", "date": activity.date or "", "min_hours": activity.min_hours or "", "max_hours": activity.max_hours or "", "frequency":activity.frequency or "", "hours_left":activity.hours_left } for activity in activities]
            # Return the activities list as JSON
            return jsonify(activities_list)
            #return jsonify(activities)
        except Exception as e:
            # Log the error
            app.logger.error(f'Error: {str(e)}')
            return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)
        
    def clear_expired(self):
        com = False
        activities = g.activities_db.query(Activity).all()
        for activity in activities:
            if activity.type == "co" or activity.type =="de":
                date_1 = dt.datetime.strptime(activity.date, r'%Y-%m-%d')
                today = dt.datetime.today()
                days_left = (date_1-today).days
                if ((activity.type == "co" and days_left < 0) or (activity.type == "de" and days_left < 1)):
                    print(f"deleted {activity.name} of type {activity.type} since there are {days_left} days left")
                    g.activities_db.delete(activity)
                    com = True
                else:
                    print(f"didnt delete {activity.name} since there are {days_left} days left")

        if com == True:
           g.activities_db.commit()

        
    def post(self):
        try:
            data = request.get_json()

            cur_activity = self.makeActivity(data)
            pre_existing = g.activities_db.query(Activity).filter(Activity.name == cur_activity.name).first()
            if  pre_existing:
                g.activities_db.delete(pre_existing)
            
            #delete activity first then re-add it
            g.activities_db.add(cur_activity)
            g.activities_db.commit()
            #create new Activity and add to database 
            
            return make_response(jsonify({'message': 'Data received successfully', 'data': data}), 200)
        except Exception as e:
            app.logger.error(f'Error: {str(e)}')
            return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)
    
    def makeActivity(self, data):
        activity = None
        match data['type']:
            case "re":
                activity = Activity(name = data['name'].strip(), type=data['type'], week_days=data['week_days'], time_pairs=data['time_pairs'])
            case "co":
                activity = Activity(name = data['name'].strip(), type=data['type'], date=data['date'], start=data['start'], end=data['end'], also_accomplishes=data['also_accomplishes'])
            case "da":
                activity = Activity(name = data['name'].strip(), type=data['type'], start=data['start'], end=data['end'], min_hours=data['min_hours'], max_hours=data['max_hours'])
            case "de":
                activity = Activity(name = data['name'].strip(), type=data['type'], date=data['date'], hours_left=data['hours_left'], min_hours=data['min_hours'], max_hours=data['max_hours'])
            case "ho":
                activity = Activity(name = data['name'].strip(), type=data['type'], frequency=data['frequency'], date=data['date'], min_hours=data['min_hours'], max_hours=data['max_hours'], start=data['start'], end=data['end'])
        return activity
        

@scheduler_ns.route('/<path:activity_name>')
class OneActivity(Resource): 
    def delete(self, activity_name):
        activity_name = activity_name.strip()
        try:
           # activities = g.activities_db.query(Activity).filter(Activity.name == activity_name).all()
            all = g.activities_db.query(Activity).all()
            activities = g.activities_db.query(Activity).filter(Activity.name == activity_name).all()
            print(activities)
            if not activities:
                return make_response(jsonify({'message': 'No activities found with the given name'}), 404)
            print("eror")
            for activity in activities:
                g.activities_db.delete(activity)
            g.activities_db.commit()

            return make_response(jsonify({'message': f"All activities with the name '{activity_name}' have been deleted successfully"}), 200)
        except Exception as e:
            app.logger.error(f'Error: {str(e)}')
            return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)
    
        
import datetime
        
@scheduler_ns.route('/authorize')
class Activator(Resource):
    def put(self):
        try:
            recurrings = g.activities_db.query(Activity).filter(Activity.type == "re").all()
            commitments = g.activities_db.query(Activity).filter(Activity.type == "co").all()
            dailies = g.activities_db.query(Activity).filter(Activity.type == "da").all()
            deadlineds= g.activities_db.query(Activity).filter(Activity.type == "de").all()
            hobbies = g.activities_db.query(Activity).filter(Activity.type == "ho").all()

            recurrings_dict = []
            for recurring in recurrings:
                recurrings_dict.append({"name": recurring.name, "type": "re", "week_days": recurring.week_days, "time_pairs": recurring.time_pairs})
            
            commitments_dict = []
            for commitment in commitments:
                commitments_dict.append({"name": commitment.name, "type": "co", "date":commitment.date, "start":commitment.start, "end":commitment.end, "also_accomplishes": commitment.also_accomplishes})
            
            dailies_dict = []
            for daily in dailies:
                dailies_dict.append({"name": daily.name, "type": "da",  "start":daily.start, "end":daily.end, "min_hours":daily.min_hours, "max_hours":daily.max_hours})
            
            deadlineds_dict = []
            for deadlined in deadlineds:
                deadlineds_dict.append({"name": deadlined.name, "type": "de", "date": deadlined.date, "hours_left": deadlined.hours_left, "min_hours": deadlined.min_hours, "max_hours": deadlined.max_hours})
                
            hobbies_dict = []
            for hobby in hobbies:
                hobbies_dict.append({"name": hobby.name, "type": "ho", "frequency": hobby.frequency, "date": hobby.date, "start":hobby.start, "end":hobby.end, "min_hours":hobby.min_hours, "max_hours":hobby.max_hours})
            
            my_scheduler = Scheduler(recurrings_dict, commitments_dict, dailies_dict, deadlineds_dict, hobbies_dict)
            events_to_schedule = my_scheduler.events

            event_scheduler.run_calendar_api(events_to_schedule)

            name = hobbies[0].type

            return make_response(jsonify({'message': f"events including '{name}' have been made"}), 200)
        except Exception as e:
            app.logger.error(f'Error: {str(e)}')
            return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)


    # def schedule_activity(self, day_int, name, start, end):





# class Finalizer:
#     def main(self, schedule):
#         self.schedule = schedule
#         #create send schedule fromthe array to google scheduler







# class Schedule_Commiter:
#     def main(schedule)
if __name__ == '__main__':
    print("Flask ENV:", app.config['ENV'])  # Add this line to check the environment
    app.run(debug=True, port=5001)