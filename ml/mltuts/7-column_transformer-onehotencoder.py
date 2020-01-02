import pandas as pd
from sklearn.preprocessing import Imputer

# Read the dataframe
df = pd.read_csv("data/missing.csv")

# Use imputer to replace missing values with mean of the column
features = df.iloc[:, :-1].values  # All rows, all but last column  (20 x 7)
labels = df.iloc[:, -1].values     # Last column values             (20 x 1)
imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
features[:, [1, 6]] = imputer.fit_transform(features[:, [1, 6]])

# Fill missing pieces of categorical information by higest frequency category
df = pd.DataFrame(features, columns=df.columns[:-1])
cols = ['Occupation', 'Employment Status', 'Employement Type']
df[cols] = df[cols].fillna(df.mode().iloc[0])


# One hot encoding

# Instead of converting categorical column into numeric enums, we can explode the
# col into N number of cols, with 1 and 0 in the values e.g.

# If the data is:
# Color    Name     Length
# Red      Apple    20
# Green    Grapes   2
# Green    Peas     1
# Orange   Orange   20
# Yellow   Banana   30
#
# We convert and explode it into
#  Red    Green    Orange    Yellow    Name    Length
#  1      0        0         0         Apple   20
#  0      1        0         0         Grapes  2
#  0      1        0         0         Peas    1
#  0      0        1         0         Orage   20
#  0      0        0         1         Banana  30
#
# This feature transformation is called one hot encoding and it fit for further
# analysis

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

features = df.iloc[:, :-1]. values

ct = ColumnTransformer([
    ('hotencoder', OneHotEncoder(), [0, 5])
], remainder="passthrough")

# ColumnTranformer takes a list of encoders and applies them on the columns mentioned
# remainder="passthrough" means those columns which are not a part of the transformations
# will be passed as it is
# Although, after the transformations, the order of columns will get changed.
# So, 0, 1, 2, 3, 4, 5 after the transformation will become
# 0(1), 0(2), 0(3), 0(4), 0(5), 0(6), 5(0), 5(1), 1, 2, 3, 4


features = ct.fit_transform(features)