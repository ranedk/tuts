import pandas as pd


# Create a dataframe from titanic.csv dataset
df = pd.read_csv("data/titanic.csv")

# Looping over Names
for name in df['Name']:
    print(name)

# Lamda transformations

# Lambda on one column
df['CleanName'] = df['Name'].apply(lambda x: x.upper())

# Lambda on all rows
df["Name_Sex"] = df.apply(lambda row: row["Name"] + " - " + str(row["Sex"]), axis = 1)

for cols in df:
    print(cols)

# Output:
#PassengerId
#Survived
#Pclass
#Name
#Sex
#Age
#SibSp
#Parch
#Ticket
#Fare
#Cabin
#Embarked
#CleanName

# To list all columns
print(df.columns)

# Iterate using index
for idx in df.index[:10]:
    print(df['Name'][idx], df['Age'][idx], df['Sex'][idx])

# Iterate using loop (when index may not be present) using loc
for i in range(10) :
  print(df.loc[i, "Name"], df.loc[i, "Age"], df.loc[i, "Sex"])

# Iterate without columns names using iloc
for i in range(10) :
  print(df.iloc[i, 3], df.iloc[i, 5], df.iloc[i, 4])

# Using row based iterator, more efficient since it yields - iterrows
# Since this converts it into Series, it doesnt preseve dtypes
# Hence should be avoided and instead use itertuples
for index, row in df.iterrows():
    print (row["Name"], row["Age"], row["Sex"])

# Using itertuples - iterates rows as namedtuples
for row in df.itertuples(index = True, name ='Pandas'):
    print (getattr(row, "Name"), getattr(row, "Age"), row.Sex)
