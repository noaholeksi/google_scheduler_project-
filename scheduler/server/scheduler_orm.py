# from sqlalchemy import create_engine, Column, types, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# meta = MetaData()
# base_activities = declarative_base(meta)
 
# class Activity(base_activities):
  
#   __tablename__ = 'activities'
#   #for all
#   activity_id    = Column(types.Integer, primary_key=True)
#   name = Column(types.String(length = 25), nullable = False)
#   type = Column(types.Enum("re", "co", "da", "de", "ho", name='type_codes'), nullable=False)

#   #just for recurring activities
#   week_days = Column(types.String(length = 25)) 
#   time_pairs = Column(types.String(length = 80))
  
#   #for hobby
#   frequency = Column(types.Integer)

#   #for a commitment, deadline, hobby
#   date = Column(types.String(length = 15))

#   #for deadlined
#   hours_left = Column(types.Integer)

#   #for commitments, daily
#   start = Column(types.String(length = 5))
#   end = Column(types.String(length = 5))

#   #for commitments
#   also_accomplishes = types.String(length = 25)

#   #for hobby, daily and  deadline
#   min_hours = Column(types.Integer)
#   max_hours = Column(types.Integer)


#   #recurring
#   #activity_id, name, type,week_days,time_pairs, 

#   #commitment
#   #activity_id, name, type, date, start, end, also_accomplishes

#   #daily
#   #activity_id, name, type, start, end, min_hours, max_hours

#   #deadlined
#   #activity_id, name, type,date, hours_left, min_hours, max_hours

#   #hobby
#   #activity_id, name, type, frequency, date, min_hours, max_hours

from sqlalchemy import create_engine, Column, types, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Define MetaData object separately
meta = MetaData()

# Create declarative base with the defined MetaData object
base_activities = declarative_base(metadata=meta)

# Define your SQLAlchemy model classes using Base
class Activity(base_activities):
    __tablename__ = 'activities'

    # Define columns here as you had them
    activity_id = Column(types.Integer, primary_key=True, autoincrement=True)
    name = Column(types.String(length=25), nullable=False)
    type = Column(types.Enum("re", "co", "da", "de", "ho", name='type_codes'), nullable=False)
    week_days = Column(types.String(length=25))
    time_pairs = Column(types.String(length=80))
    frequency = Column(types.Integer)
    date = Column(types.String(length=15))
    hours_left = Column(types.Integer)
    start = Column(types.String(length=5))
    end = Column(types.String(length=5))
    also_accomplishes = Column(types.String(length=25))
    min_hours = Column(types.Integer)
    max_hours = Column(types.Integer)

# Add more SQLAlchemy model classes as needed

