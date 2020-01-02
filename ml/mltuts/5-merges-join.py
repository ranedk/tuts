import pandas as pd
import numpy as np


# Define dataframes

students = pd.DataFrame({
    'name': ['Devendra', 'Prem', 'Kiran', 'Manish', 'Sandeep', 'Deepika', 'Amit'],
    'class': ['7A', '7B', '7D', '7A', '7B', '7B', '7C'],
    'gender': ['M', 'M', 'F', 'M', 'M', 'F', 'M'],
    'roll': [1, 2, 3, 4, 5, 6, 7]
}).set_index('roll')

physics = pd.DataFrame({
    'roll': [2, 4, 5, 6, 7],
    'marks': [32, 65, 43, 98, 43],
}).set_index('roll')

chemistry = pd.DataFrame({
    'roll': [1, 2, 3, 4, 5, 6, 7, 100, 101, 103],
    'marks': [32, 65, 43, 98, 43, 87, 76, 34, 76, 87],
})

maths = pd.DataFrame({
    'sr': [1, 2, 3, 5, 6],
    'marks': [45, 23, 76, 87, 45],
}).set_index('sr')


# Inner join (default) - Intersection
pd.merge(students, physics, on="roll")
# Output
#2        Prem    7B      M     32
#4      Manish    7A      M     65
#5     Sandeep    7B      M     43
#6     Deepika    7B      F     98
#7        Amit    7C      M     43

# Left join - All students shown, NaN for missing entries in subject table
pd.merge(students, physics, on="roll", how="left")
# Output
#1     Devendra    7A      M    NaN
#2         Prem    7B      M   32.0
#3        Kiran    7D      F    NaN
#4       Manish    7A      M   65.0
#5      Sandeep    7B      M   43.0
#6      Deepika    7B      F   98.0
#7         Amit    7C      M   43.0

# Outer join - All  shown, NaN for missing entries in either tables
pd.merge(students, chemistry, on="roll", how="outer")
# Output
#0     1  Devendra    7A      M     32
#1     2      Prem    7B      M     65
#2     3     Kiran    7D      F     43
#3     4    Manish    7A      M     98
#4     5   Sandeep    7B      M     43
#5     6   Deepika    7B      F     87
#6     7      Amit    7C      M     76
#7   100       NaN   NaN    NaN     34
#8   101       NaN   NaN    NaN     76
#9   103       NaN   NaN    NaN     87

# If the columns names are differet, use left_on and right_on
# pd.merge(students, maths, left_on="roll", right_on="sr", how='left')
# This will give an error since 'roll' and 'sr' are in index and not in columns.
# Instead use
pd.merge(students, maths, left_index=True, right_index=True, how='left')