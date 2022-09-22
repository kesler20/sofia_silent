
import pandas as pd
import time
import numpy as np
import json
from logs_diet.diet_logging import logger
''''
    Assumptions:
    Units of ammount assumes 1L = 1Kg of substance
    Every protein/calorie is standardised per units of ammount
'''

class Food(dict):

    def __init__(self, name, cost, protein, calories, taste):
        self['Name'] = [name]
        self['Cost (£)'] = [cost]
        self['protein (g/ammount)'] = [protein]
        self['calories (g/ammount)'] = [calories]
        self['taste'] = [taste]

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            self['Cost (£)'] = self['Cost (£)'][0] * other
            self['protein (g/ammount)'] = self['protein (g/ammount)'][0] * other
            self['calories (g/ammount)'] = self['calories (g/ammount)'][0] * other
        return self
    
    def __repr__(self):
        return f''''
            {self['Name'][0]}(
                Cost (£) : {self['Cost (£)'][0]},
                protein (g/ammount) : {self['protein (g/ammount)'][0]},
                calories (kcal) : {self['calories (g/ammount)'][0]},
                taste score 1/5: {self['taste'][0]}
            )
        '''

    def __add__(self, other):
        if type(other) == type(self):
            return {*self, *other}
        else:
            raise TypeError

# class Meal(object):

#     def __init__(self, name, type_of_meal, sum_of_foods):
#         self.name: str = f'{name} ({type_of_meal})'
#         self.recipe = sum_of_foods
#         self.values = self.create_meal()

#     def __add__(self, other):
#         # assumes that the total value has not being computed yet
#         if type(other) == type(self):

#             df = pd.DataFrame({f'{self.name}, {other.name} - {str(time.strftime("%d/%m/%Y"))}': [
#                               i for i in range(len(self.values) + len(other.values))]})

#             columns = list(self.values.columns)
#             for col in columns:
#                 if col == self.name:
#                     pass
#                 else:
#                     column_values = []
#                     for old_val in self.values[col]:
#                         column_values.append(old_val)

#                     for new_val in other.values[col]:
#                         column_values.append(new_val)

#                     df[col] = pd.DataFrame(column_values)

#             return df
#         else:
#             raise TypeError

#     def create_meal(self):
#         keys = list(self.recipe.keys())
#         meal = pd.DataFrame(
#             {f'{self.name}': [i for i in range(len(self.recipe[keys[0]]))]})
#         for key in keys:
#             meal[key] = self.recipe[key]

#         return meal

#     def get_total_values(self):
#         array = self.values.values.T
#         total_values = []
#         for arr in array[1:]:
#             try:
#                 total_values.append(sum(arr))
#             except TypeError:
#                 pass

#         # this is to make it of the same lenght of the array
#         total_values.insert(0, np.nan)
#         total_values.insert(0, 'total values:')
#         return total_values

class Meal(object):

    def __init__(self, name, foods):
        self.name: str = name
        self.foods: 'list[Food]' = foods

    def __repr__(self):
        return f'''
        {self.name},
            {self.foods}
        '''

    def __hash__(self):
        return hash((food for food in self.foods))

class Diet(object):

    def __init__(self, name, sum_of_meals=pd.DataFrame([i for i in range(10)])):
        self.name = name
        self.values = sum_of_meals

    def get_total_values(self):
        array = self.values.values.T

        total_values = []
        for arr in array[1:]:
            try:
                total_values.append(sum(arr))
            except TypeError:
                pass

        total_values.append(total_values[-1]/len(self.values))
        total_values.remove(total_values[-2])

        # this is to make it of the same lenght of the array
        total_values.insert(0, np.nan)
        total_values.insert(0, 'total values:')
        return total_values

