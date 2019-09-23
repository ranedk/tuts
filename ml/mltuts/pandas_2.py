import pandas as pd


# Create a dataframe from titanic.csv dataset
df = pd.read_csv("data/titanic.csv")

# Shows details of the dataframe - columns, total rows, non-null counts
print(df.info())

# Initial rows of a dataset
print(df.head())
# End 4 rows of a dataset
print(df.tail(4))

# column count and row count of a dataframe
print(df.shape)

# 4th row of dataframe
print(df.iloc[0])

# 5th row, 6th col of dataframe
print(df.iloc[5][6])

# 4th to 10th rows of dataframe
print(df.iloc[4:7])

# 4th to 7th row of dataframe, with only the 3rd col
print(df.iloc[4:7, 3])

# 4th to 7th row of dataframe, with 3rd to 7th cols
print(df.iloc[4:7, 3:7])

# Rest works like list slicing
print(df.iloc[-20:-1: 2, 3:9:2])

# Instead of auto-increment indexes, you can change index to a col
df0 = df.set_index(df['Name'])

# Index based lookup, using loc
print(df0.loc['Dooley, Mr. Patrick'])

# Index is not required to be unique
df1 = df.set_index(df['Sex'])

# Index based lookup
print(df1.loc['male'])

# Conditional lookups and filter
print(df[df['Pclass'] == 2])

print(df[(df['Pclass'] == 3) & (df['Sex'] == 'male')])

print(df[(df['Age'] > 43) & (df['Sex'] == 'male')])

# Add a new column based on old columns
df['Class Type'] = df['Pclass'].replace(1, 'First').replace(2, 'Second').replace(3, 'Third')

df['demography'] = df[]


# Rename columns
df = df.rename(columns={'Sex': 'Gender'})

# Functions on columns
print(
      "\nmean age=                ", df['Age'].mean(),
      "\nmax age=                 ", df['Age'].max(),
      "\ncount of non-null ages=  ", df['Age'].count(),
      "\nsum of all ages=         ", df['Age'].sum()
)

print(
      "\nUnique values of gender        ", df['Gender'].unique(),
      "\nUnique value counts of gender  ", df['Gender'].value_counts()
)

# Rows or Series
row = df.loc[4]         # type(row) == pandas.core.series.Series

print("null columns: ", row.isnull())

print("non null columns: ", row.notnull())

# One can do a lot of operations on Series too. row.count(), row.sum() etc.

print("All rows with null in Ages  = ",  df[df['Age'].isnull()])

# Dropping the PassengerId column => find passengerId col, drop along axis=1
passenger_removed = df.drop(['PassengerId', 'Cabin'], axis=1)

# Remove by column index
3_col_removed = df1.drop(df1.columns[3], axis=1)

# Remove multiple columns by indexes
368_col_removed = df1.drop(df1.columns[[3,6,8]], axis=1)

# Axis = 1 is columns, Axis = 0 is rows
# Remove rows with index 0,2,4,6,8
rows_removed = df.drop([0, 2, 4, 6, 8], axis=0)

# Change index and remove by index
df1 = df.set_index('Age')
rows_removed_1 = df1.drop(['60', '40.5', '30.5'], axis=0)






