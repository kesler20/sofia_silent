from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlalchemy
from xml.dom import NotFoundErr
import logging
import sys
import os
import datetime

logging.basicConfig(
    filename=r"C:\Users\Uchek\Protocol\Sofia\logs_src\main_logs.log",
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s)'
)

try:
    from flask_database import FORMAT_SESSION_ID, db, DailySessiion, WorkoutDatabase, Finances, Weight, Meals, Foods
    from logs_src.main_logging import logger
    from Gym.training import Exercise, Workout
    from Diet.meals import Meal, Food

except ModuleNotFoundError as err:

    def check_directory(path: str):
        if path.startswith('.') or path.startswith('__') or path.endswith('.exe'):
            return False
        else:
            return True
    _modules = list(filter(check_directory, os.listdir(os.getcwd())))

    for module in _modules:
        sys.path.append(os.path.join(os.getcwd(), module))

    logging.info('----------- Modules in System Path ------------')
    logging.info(sys.path)

    from main_logging import logger
    from training import Exercise, Workout
    from flask_database import FORMAT_SESSION_ID, db, DailySessiion, WorkoutDatabase, Finances, Weight, Meals, Foods
    from meals import Meal, Food


class DatabaseContexManager(object):

    def __init__(self, *args):
        self.name = args[0]
        self.args = args
        self.db: SQLAlchemy = db

    def __enter__(self):
        self.db.create_all()

        if self.name == 'daily_session':
            self.table = DailySessiion(
                date_id=datetime.date.today(),
                workout=self.args[1],
                finances=self.args[2],
                weight=self.args[3],
                diet=self.args[4]
            )

        elif self.name == 'Workouts':
            self.table = WorkoutDatabase(
                date_id=datetime.date.today(),
                session_id=self.args[1],
                content=self.args[2]
            )

        elif self.name == 'Finances':
            self.table = Finances(
                date_id=datetime.date.today(),
                session_id=self.args[1],
                food_cost=self.args[2],
                travel_costs=self.args[3],
                other_costs=self.args[4]
            )

        elif self.name == 'Weight':
            self.table = Weight(
                date_id=datetime.date.today(),
                session_id=self.args[1],
                weight=self.args[2],
                body_fat=self.args[3],
                maintanance_calories=self.args[4]
            )

        elif self.name == 'Foods':
            self.table = Foods(
                name=self.args[1],
                date_id=datetime.date.today(),
                session_id=self.args[2],
                protein=self.args[3],
                calories=self.args[4],
                food_cost=self.args[5]
            )

        elif self.name == 'Meals':
            self.table = Meals(
                name=self.args[1],
                date_id=datetime.date.today(),
                session_id=self.args[2],
                content=self.args[3]
            )

        else:
            logger.error(
                'The name proivided does not correspond to any database table')
            raise NotFoundErr

        return self.table

    def __exit__(self, exec_type, exec_val, traceback):
        try:
            self.db.session.add(self.table)
            self.db.session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            logger.error(err)
            logger.info(
                'this could be cause the table has already been created')

    def __repr__(self):
        return f'''
            {self.name}(
                self.date_id : {datetime.date.today()},
                session id : {self.args[1]},
                content : {self.args[2:]}
            )
        '''


def add_workout_to_database(filename=None):
    if filename is None:
        filename = r"C:\Users\CBE User05\Protocol\Sofia\Database\Files\training.csv"

    df = pd.read_csv(filename)

    logger.info('----workout loaded successfully--------')
    logger.info(df)
    workout_ = list(
        zip(df.columns, df.values[0], df.values[1], df.values[2]))[1:]
    workout_summary = Workout(
        [Exercise(exercise[0], *exercise[1:]) for exercise in workout_])

    with DatabaseContexManager('Workouts', ('workouts', datetime.datetime.now().strftime(FORMAT_SESSION_ID)), workout_summary) as data_base:
        logger.info(data_base)

    logger.info(
        f"workout {('workout', datetime.datetime.now().strftime(FORMAT_SESSION_ID))} loaded succesfully")


def add_meal_to_database(name: str, meal: Meal):

    with DatabaseContexManager('Meals', name, ('Meals', datetime.datetime.now().strftime(FORMAT_SESSION_ID)), meal) as data_base:
        print(data_base)
        logger.info(data_base)

    logger.info(
        f"meal {('meal', datetime.datetime.now().strftime(FORMAT_SESSION_ID))} loaded succesfully")


def broadcast_meals_from_database():
    db.create_all()
    return db.session.query(Meals).all()


def add_food_to_database(name: str, protein: int, calories: int, food_cost: int):
    session_id = ('Foods', datetime.datetime.now().strftime(FORMAT_SESSION_ID))
    with DatabaseContexManager('Foods', name, session_id, protein, calories, food_cost) as data_base:
        print(data_base)
        logger.info(data_base)

    logger.info(
        f"meal {('meal', datetime.datetime.now().strftime(FORMAT_SESSION_ID))} loaded succesfully")


def broadcast_foods_from_database():
    db.create_all()
    return db.session.query.filter_by(name='choicolate').first()

#TODO: fix the database connection as you cannot add load and remove objects from it