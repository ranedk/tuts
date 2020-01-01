import pandas as pd
import numpy as np

# Create a timeseries data

# Create a time series array. Start as 01/01/2018, 2000000 data points at a
# delta of 60 seconds
ts_index = pd.date_range('01/01/2018', periods=200000, freq='60S')

# Use the range to create index for dataframe
df = pd.DataFrame(index=ts_index)

# Add a column, NumberOfVehicles, which signfies the number of vehicles passing
# very 60 seconds through a junction

df['NumberOfVehicles'] = np.random.randint(0, 20, 200000)  # 2000000 pts between 0 and 20

# Since the INDEX is timeseries, we can do timeseries calculation

# Sum by grouping/sampling weeks data together
df.resample('W').sum()

# resample by default does it on index, if the column wasn't index, we use:
# df.resample('W', on='NumberOfVehicles').sum()

# Sum by grouping/sampling two weeks data together
df.resample('2W').sum()

# Sum by grouping/sampling monthly data together
df.resample('M').sum()
# Output
#2018-01-31            424438
#2018-02-28            380936
#2018-03-31            424328
#2018-04-30            408898
#2018-05-31            260404

# Sum by grouping/sampling monthly data together, the labels will be the
# end of the month, otherwise its the start of the month
df.resample('M', label='left').sum()
# Output
#2017-12-31            424438
#2018-01-31            380936
#2018-02-28            424328
#2018-03-31            408898
#2018-04-30            260404

# Lets make a field which is not the index, but is another column
df['DateTime'] = df.index

# Adding new datetime fields to the dataframe
df['Year'] = df['DateTime'].dt.year
# If you want to use the index column, use
# df['Year'] = df.index.year

df['Month'] = df.DateTime.dt.month

df['Day'] = df.DateTime.dt.day

df['WeekDay'] = df.DateTime.dt.weekday_name
# Output
#                     NumberOfVehicles            DateTime  ...  Day   WeekDay
#2018-01-01 00:00:00                18 2018-01-01 00:00:00  ...    1    Monday
#2018-01-01 00:01:00                 2 2018-01-01 00:01:00  ...    1    Monday
#2018-01-01 00:02:00                10 2018-01-01 00:02:00  ...    1    Monday