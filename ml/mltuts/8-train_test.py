import pandas as pd
from sklearn.preprocessing import Imputer

# Read the dataframe and clean up the data (missing values and encoding)
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
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

features = df.iloc[:, :-1]. values

ct = ColumnTransformer([
    ('hotencoder', OneHotEncoder(), [0, 5])
], remainder="passthrough")

features = ct.fit_transform(features)

# We not have features and labels, we need to train using a training set

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    features,
    labels,
    test_size=0.25,     # Percentage of data to use as training set
    random_state=0,     # Seed used by random number generator
)

# features.shape    (20, 13)            labels.shape    (20, )
# X_test.shape      (5, 13)             y_test.shape    (5, )
# X_train.shape     (15, 13)            y_train.shape   (15, )