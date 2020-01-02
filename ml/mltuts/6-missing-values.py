import pandas as pd

# Load data with missing values
df = pd.read_csv("data/missing.csv")
#   Country   Age  Gender  ... Employement Type   Salary Purchased
#0   Poland  34.0    Male  ...        Permanent  72000.0        No
#1    Spain  42.0  Female  ...        Temporary  48000.0       Yes
#2  Germany  29.0    Male  ...        Temporary  54000.0        No
#3    Spain  38.0    Male  ...        Permanent  61000.0        No
#4  Germany  32.0    Male  ...        Permanent      NaN       Yes


# Removing rows with missing values

df.isnull().sum()
# Output
#Country              0
#Age                  3
#Gender               0
#Occupation           2
#Employment Status    3
#Employement Type     3
#Salary               4
#Purchased            0

cols_without_missing_values = df.dropna(axis=1)

row_without_missing_values = df.dropna(axis=0)

names_of_cols_with_missing_values = [col for col in df if df[col].isnull().any()]

# Imputer strategy to deal with NaN

# Data fitting to fill-in missing values
# Features (X)
# Labels (y) aka Dependent variable
# 
# For df, All cols are features except Purchased, which is the Label

features = df.iloc[:, :-1].values  # All rows, all but last column  (20 x 7)
labels = df.iloc[:, -1].values     # Last column values             (20 x 1)

from sklearn.preprocessing import Imputer

# Replacing numeric values

# Use mean of axis=0 to replace missing values denoted by NaN
imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)

# fit along 1 and 6 column of features
imputer.fit(features[:, [1,6]])    # strategy is mean, so will only with numbers

# replace features with the transformed values
features[:, [1, 6]] = imputer.fit_transform(features[:, [1, 6]])

# Create dataframe from array of features
missing_values_replaced_by_mean = pd.DataFrame(features)

# Replacing non-numberic values
cols = ['Occupation', 'Employment Status', 'Employement Type']

# Find the highest frequency values
df.mode()
#   Country   Age Gender  ... Employement Type   Salary Purchased
#0  Germany  38.0   Male  ...        Temporary  48000.0       Yes
#1    Spain   NaN    NaN  ...              NaN  52000.0       NaN
#2      NaN   NaN    NaN  ...              NaN  54000.0       NaN

# Replace all NAs with max-frequency label
df[cols] = df[cols].fillna(df.mode().iloc[0])



# Label encoding: Making enums from text categorical items
# Requires no NaN in the data

from sklearn.preprocessing import LabelEncoder

features = df.iloc[:, :-1].values

encode = LabelEncoder() 

# 0 columns is the country, which is text
features[:, 0] = encode.fit_transform(features[:, 0])

pd.DataFrame(features)
#    0    1       2         3    4              5      6
#0   4   34    Male  Salaried  Yes      Permanent  72000
#1   5   42  Female  Business  Yes      Temporary  48000
#2   2   29    Male  Business   No      Temporary  54000
#3   5   38    Male  Business   No      Permanent  61000

for col in [2, 3, 4, 5]:
    features[:, col] = encode.fit_transform(features[:, col])
    
pd.DataFrame(features)
#    0    1  2  3  4  5      6
#0   4   34  1  1  1  0  72000
#1   5   42  0  0  1  2  48000
#2   2   29  1  0  0  2  54000
#3   5   38  1  0  0  0  61000