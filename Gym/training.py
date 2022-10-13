import pandas as pd
from pandas import DataFrame
import random
import time
import os
import datetime
import pandas
from interfaces.os_interface import OperatingSystemInterface

osi = OperatingSystemInterface()

EXERCISE_PATH = os.path.join(osi.gcu(), 'OneDrive', 'Documents', 'exercises.csv')
TRAINING_PATH = os.path.join(osi.gcu(), 'OneDrive', 'Documents', 'training.csv')
today = datetime.date.today().weekday()


def construct_exercise(name):
    try:
        df = pd.read_csv(EXERCISE_PATH)
    except pandas.errors.EmptyDataError:
        df = pd.DataFrame([0, 0, 0])
    df[name] = pd.DataFrame([0, 0, 0])
    print(df)
    df.to_csv(EXERCISE_PATH, index=False)


class Exercise(object):

    def __init__(self, name, weight=None, sets=None, reps=None):
        self.name = name
        self.weight = weight
        self.sets = sets
        self.reps = reps
        try:
            df = pd.read_csv(EXERCISE_PATH)
            if self.weight == None and self.sets == None and self.reps == None:
                self.weight = df[self.name][0]
                self.sets = df[self.name][1]
                self.reps = df[self.name][2]
        except KeyError:
            print('constructing exercise....')
            construct_exercise(name)
        except pandas.errors.EmptyDataError:
            print('constructing exercise....')
            construct_exercise(name)

    def __repr__(self):
        return f'''
        name : {self.name},
        weight: {self.weight} Kg,
        sets: {self.sets},
        reps: {self.reps}       
        '''

    def record_weight(self):
        pass


class Workout(list):

    def __init__(self, exercises):
        self.exercises: 'list[Exercise]' = exercises

    def __repr__(self):
        return f'''
            {self.exercises}
        '''

    def __hash__(self):
        return hash((exercise for exercise in self.exercises))

    def check_if_workout_valid(self):
        unique_exercise_workout = []
        for exercise in self.exercises:
            if exercise in unique_exercise_workout:
                pass
            else:
                unique_exercise_workout.append(exercise)
        if len(unique_exercise_workout) != len(self.exercises):
            return False
        else:
            return True

    def record_workout(self):
        pass


# turn the contents of this list as exercises
biceps_heavy: list = [
    Exercise('heavy barbel curl'), Exercise('heavy preacher curl')]
biceps_light: list = [Exercise('superman curl'), Exercise(
    'inclined bench bicep curl superset'), Exercise('hammer curl superset'), Exercise('bicep cable curl')]
triceps_heavy: list = [Exercise('heavy deeps'), Exercise('overhead tricpes with 1 dumbell'), Exercise(
    'easy bar heavy tricepts extensions'), Exercise('heavy cable'), Exercise('dumbell overhead tricpes')]
triceps_light: list = [Exercise('cable tricep pushdown triplesuperset close weights'), Exercise(
    'triceps straight bar supersets')]
shoulders_heavy: list = [
    Exercise('military press'), Exercise('heavy shoulder press')]
shoulders_light: list = [Exercise('front and lateral raises w cables'), Exercise(
    'lateral raises w dumbell superset'), Exercise('seated military press'), Exercise('arnold shoulder press')]
back_heavy: list = [Exercise('heavy chin ups'), Exercise(
    'barbell rows'), Exercise('heavy lat pull downs')]
back_light: list = [Exercise('lat pull downs controlled'), Exercise(
    'changed grip lat pull down'), Exercise('pull ups'), Exercise('chin ups')]
abdominals: list = [Exercise('leg raises'), Exercise(
    'L seats'), Exercise('crunches'), Exercise('lateral leg rasies')]
chest: list = [Exercise('bench')]

# the form will tell you the exercises and inser as a placeholder the previous weight sets and reps that you have done
# then you will only have to fill in the form and huit record #

gym_schedule: list = [
    [chest, biceps_heavy, triceps_heavy, biceps_light,
        triceps_heavy, abdominals, biceps_light, triceps_light],
    'rest',
    [back_heavy, shoulders_heavy, abdominals, back_light,
        shoulders_light, abdominals, back_light, shoulders_light],
    'rest',
    [chest, biceps_heavy, triceps_heavy, abdominals, biceps_light,
        triceps_heavy, abdominals, biceps_light, triceps_light],
    [back_heavy, shoulders_heavy, abdominals, back_light,
        shoulders_light, abdominals, back_light, shoulders_light],
    'rest'
]


def generate_workout():
    valid_workout = False  # a valid workout should have no repeats
    while not valid_workout:
        workout = Workout([])
        for muscle_group in gym_schedule[today]:
            if gym_schedule[today] == 'rest':
                workout.exercises = []
            else:
                n = random.randint(0, len(muscle_group) - 1)
                workout.exercises.append(muscle_group[n])
        valid_workout = workout.check_if_workout_valid()
    print(workout)
    return workout


def write_generated_workout_to_csv(workout: Workout, save=True):
    workout_summary = pd.DataFrame([i for i in range(3)])
    workout_summary[str(time.strftime("%d/%m/%Y"))
                    ] = ['weight (Kg)', 'sets', 'reps']
    for exercise in workout.exercises:
        print(exercise)
        name = exercise.name
        weight = exercise.weight
        sets = exercise.sets
        reps = exercise.reps
        workout_summary[name] = [weight, sets, reps]

    workout_summary.drop([0], axis=1, inplace=True)

    print(workout_summary)
    if save:
        workout_summary.to_csv(TRAINING_PATH, index=False)
        print('------workout saved succesfully------------')
    else:
        return workout_summary


def update_exercises_results():
    try:
        training_results: DataFrame = pd.read_csv(TRAINING_PATH)
    except FileNotFoundError as err:
        print(err)
        return None
    historical_training_database: DataFrame = pd.read_csv(EXERCISE_PATH)
    columns_from_historical = list(historical_training_database.columns)
    for column in columns_from_historical:
        for name in training_results.columns:
            column = str(column)
            name = str(name)
            if name.startswith(column):
                print(name)
                print(column)
                try:
                    if sum(historical_training_database[column]) > sum(training_results[name]):
                        pass
                    else:
                        historical_training_database[column] = training_results[name]
                        print(historical_training_database[column])
                except TypeError:
                    pass
    print('-------------------results updated succesfully--------------')
    historical_training_database.to_csv(EXERCISE_PATH, index=False)
