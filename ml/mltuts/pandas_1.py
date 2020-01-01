import pandas as pd
import numpy as np

# Create a new dataframe
df0 = pd.DataFrame()

# Adding data to dataframe - column by column
# All data must be present, else error
df0['name'] = ['Devendra', 'Deepak', 'Amit']
df0['language'] = ['Javascript', 'Python', 'Rust']
df0['age'] = [37, 38, np.NAN]

print(df0)
# dataframes assign an auto-increment index to each row

# Adding a row - new dataframe is generated
df0 = df0.append(
    pd.Series(['Aniket', 'Python', 34], index=['name', 'language', 'age']),
    ignore_index=True
)
# ignore_index=True, means add the series with a auto-increment row-index

print(df0)

df0 = df0.append(
    pd.Series(
        ['Rakesh', 'Javascript', 31, 'Design'],
        index=['name', 'language', 'age', 'department']
    ),
    ignore_index=True
)
# add a department column to dataframe, makes it NaN for previous entries

print(df0)

# To understand nuisances for ignore_index check the link
# https://stackoverflow.com/questions/32801806/pandas-concat-ignore-index-doesnt-work

