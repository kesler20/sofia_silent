from flask import Flask
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from datetime import date

todays_date = date.today()
day = int(todays_date.strftime('%d'))

month = int(todays_date.strftime('%m')[1])
if month == 0:
    month = int(todays_date.strftime('%m'))   

def is_odd(x):
    return x%2 != 0 

FORMAT_SESSION_ID = "%d/%m/%Y"

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(),'templates'),
    static_folder=os.path.join(os.getcwd(),'static')
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kesler-isoko.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class File(object):

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exec_type, exec_val, traceback):
        self.file.close()

class DailySessiion(db.Model):
    __tablename__ = 'daily_session'
    date_id = Column(DateTime, primary_key=True,
                     nullable=False, default=datetime.datetime.now().strftime(FORMAT_SESSION_ID))
    workout = relationship('WorkoutDatabase', backref='date', lazy=True)
    finances = relationship('Finances', backref='date', lazy=True)
    weight = relationship('Weight', backref='date', lazy=True)
    food = relationship('Foods', backref='date', lazy=True)
    meal = relationship('Meals', backref='date', lazy=True)

    def __repr__(self):
        return f'''
        DailySessiion(
                date_id : {self.date_id},
                workout : {self.workout},
                finances: {self.finances},
                weight : {self.weight},
                diet : {self.diet}
            )
        '''

class WorkoutDatabase(db.Model):

    session_id = Column(JSON, primary_key=True, nullable=False,
                        default=('Workout',datetime.datetime.now().strftime(FORMAT_SESSION_ID)))
    content = Column(JSON, nullable=False, default=tuple(()))
    date_id = Column(DateTime, ForeignKey(
        'daily_session.date_id'), nullable=False)

    def __repr__(self):
        return f'''
            Workout(
                date : {self.date_id},
                session id : {self.session_id},
                content: {self.content}
            )
        '''
        
class Finances(db.Model):

    session_id = Column(JSON, primary_key=True, nullable=False,
                        default=('Finances',datetime.datetime.now().strftime(FORMAT_SESSION_ID)))
    food_cost = Column(Integer, ForeignKey('foods.food_cost'), nullable=False)
    travel_costs = Column(Integer, primary_key=True, nullable=False, default=0)
    other_costs = Column(Integer, primary_key=True, nullable=False, default=0)
    date_id = Column(DateTime, ForeignKey(
        'daily_session.date_id'), nullable=False)

    def __repr__(self):
        return f'''
            Finances(
                date : {self.date_id},
                session id : {self.session_id},
                food_cost : {self.food_cost}
                travel_costs : {self.travel_costs}
                other_costs : {self.other_costs}
            )
        '''

class Weight(db.Model):

    session_id = Column(JSON, primary_key=True, nullable=False,
                        default=('Weight',datetime.datetime.now().strftime(FORMAT_SESSION_ID)))
    weight = Column(Integer, nullable=False, default=85)
    body_fat = Column(Integer, nullable=False, default=17)
    maintanance_calories = Column(Integer, nullable=False, default=2000)
    date_id = Column(DateTime, ForeignKey(
        'daily_session.date_id'), nullable=False)

    def __repr__(self):
        return f'''
            Health(
                date : {self.date_id},
                session id : {self.session_id},
                weight : {self.weight},
                body_fat = {self.body_fat},
                maintanance_calories = {self.maintanance_calories}
            )
        '''

class Foods(db.Model):

    session_id = Column(JSON, primary_key=True, nullable=False,
                        default=('Food',datetime.datetime.now().strftime(FORMAT_SESSION_ID)))
    name = Column(String, nullable=False, default='this')
    protein = Column(Integer, nullable=False, default=180)
    calories = Column(Integer, nullable=False, default=2000)
    food_cost = Column(Integer, nullable=False, default=7)
    date_id = Column(DateTime, ForeignKey(
        'daily_session.date_id'), nullable=False)

    def __repr__(self):
        return f'''
            Food(
                Name : {self.name},
                date : {self.date_id},
                session id : {self.session_id},
                protein : {self.protein}
                calories : {self.calories}
                food cost: {self.food_cost}
            )
        '''
class Meals(db.Model):
    
    session_id = Column(JSON, primary_key=True, nullable=False,
                        default=('Meal',datetime.datetime.now().strftime(FORMAT_SESSION_ID)))
        
    name = Column(String, nullable=False, default='this')
    content = Column(JSON, nullable=False, default=tuple(()))
    date_id = Column(DateTime, ForeignKey(
        'daily_session.date_id'), nullable=False)

    def __repr__(self):
        return f'''
            Meal(
                name : {self.name},
                date : {self.date_id},
                session id : {self.session_id},
                content: {self.content}
            )
        '''
    