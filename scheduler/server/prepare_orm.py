import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .scheduler_orm import base_activities, Activity
from .util import get_config

import click
from flask import Flask

import csv
#from datetime import datetime, date

app = Flask(__name__)


@app.cli.command('init-db')
def init_db():
    config = get_config(os.environ['FLASK_ENV'], open('server/config.yaml'))
    db   = create_engine(config['DB_ACTIVITIES'])
    base_activities.metadata.create_all(db)
    
    Session = sessionmaker(db)
    session = Session()
    if session.query(Activity).count() == 0:
        data = []
        R = csv.reader(open('activities.csv', encoding='utf8'))
        for row in R:
            if len(row[4]) <= 500:
                data.append(process_row(row))

        print('Adding', len(data), 'rows to Activity table')
        session.add_all(data)
        session.commit()


def process_row(row):
    type = int(row[2])
    activity = None
    match type:
        #recurring
        case 1: #activity_id, name, type, week_days,time_pairs, 
            activity = Activity(id = int(row[0]), name = row[1], type = int(row[2]),
                                week_days = row[3], time_pairs = row[4])

        #commitment
        case 2: #activity_id, name, type, date, start, end, also_accomplishes
            activity = Activity(id = int(row[0]), name = row[1], type = int(row[2]), 
                                date = row[3], start = row[4], end = row[5], also_accomplishes = row[6])
        #daily 
        case 3: #activity_id, name, type, start, end, min_hours, max_hours
            activity = Activity(id = int(row[0]), name = row[1], type = int(row[2]), 
                                start = row[3], end = row[4],
                                min_hours = float(row[5]), max_hours = float(row[6]))

        #deadlined
        case 4: #activity_id, name, type,date, hours_left, min_hours, max_hours
            activity = Activity(id = int(row[0]), name = row[1], type = int(row[2]), 
                                date = row[3], hours_left = float(row[4]), 
                                min_hours = float(row[5]), max_hours = float(row[6]))

        #hobby   
        case 5: #activity_id, name, type, frequency, date, min_hours, max_hours
            activity = Activity(id = int(row[0]), name = row[1], type = int(row[2]), 
                                frequency = int(row[3]), date = row[4], 
                                min_hours = float(row[5]), max_hours = float(row[6]))

    return activity