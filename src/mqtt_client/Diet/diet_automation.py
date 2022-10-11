# include weight and use poandas and matplotlib to plot calories and protein and weight
import myfitnesspal
from datetime import date


class CalorieCounter(object):

    def __init__(self):

        self.client = myfitnesspal.Client(
            'dollyoung20', password='kesler isoko20')

        todays_date = date.today()
        self.today = todays_date
        day = int(todays_date.strftime('%d'))

        month = int(todays_date.strftime('%m')[1])
        if month == 0:
            month = int(todays_date.strftime('%m'))

        self.day = self.client.get_date(2021, month, day)
        self.breakfast = self.day.meals[0]
        self.lunch = self.day.meals[1]
        self.dinner = self.day.meals[2]
        self.snack = self.day.meals[3]

    def __str__(self):
        return f'''
            day : {self.day.totals},
            breakfast foods: {self.breakfast.entries[0:len(self.breakfast.entries)]},
            breakfast: {self.breakfast.totals},
            lunch foods: {self.lunch.entries},
            lunch: {self.lunch.totals},
            dinner foods: {self.dinner.entries},
            dinner: {self.dinner.totals},
            snack foods: {self.snack.entries}
            snack: {self.snack.totals}
            '''

    def yesterdays_recap(self):

        yeserdays_date = date.today()
        day = int(yeserdays_date.strftime('%d')) - 1
        month = int(yeserdays_date.strftime('%m')[1])
        if month == 0:
            month = int(self.today.strftime('%m'))
            logger.info(month)

        self.day = self.client.get_date(2021, month, day)
        logger.info(self)


calories = CalorieCounter()
logger.info(calories)
