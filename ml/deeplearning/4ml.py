# Supervised: Generalize from a set training data. Training data to classify 
# Unsupervised: Find structure in data. Group data by attributes
# Reinforcement: Learning behaviour in environment. Win a videogame


# 1. Linear regressing with neural networks

# Sample problem statement: Fit a y = wX + b line.
# We create a problem statement such that input X consists of N dimensions and Output y is single dimension

# Given a weight to height datafrae df, to create a model predict w and b

import pandas as pd


X = df[['Height']].values   # Note the [[ instead of simple array of height values, we get
                            # a array with each item being a coordinate in 1 dimension space [[x1], [x2], [x3], [x4]]
                            # The generalised format will be m points, n dimensions [[x11,x12... x1n]... [x21, x22... xmn]]
                            # m x n matrix = m points, n dimensions

y_true = df['Weight'].values    # this is a straight forward array of weight values [y1, y2.... ym]

# support y_pred is the values predicted by the model for all values X
# The optimization function is to find w and b to minimize mean_squared_error

def mean_squared_error(y_true, y_pred):
    s = (y_true - y_pred)**2
    return s.mean()

# Solving the optimization problem

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam, SGD

model = Sequential()    # Define model for keras
model.add(Dense(1, input_shape=(1,)))   # Define Dense, which implements linear model y = wX + b
                                        # input_shape is (1, ) and the dimentionality of output space is 1

model.summary()
"""
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
dense (Dense)                (None, 1)                 2
=================================================================
Total params: 2
Trainable params: 2
Non-trainable params: 0
_________________________________________________________________
"""

# The 2 output params are w and b

model.compile(Adam(lr=0.8), 'mean_squared_error')  # Takes Adam optimizer and minimize the mean_squared_error

# Train the model
model.fit(X, y_true, epochs=40, verbose=0);

# Get output of predictions
y_pred = model.predict(X)

W, B = model.get_weights()  # Get w and b as parameters to the model
                            # In this case w will be a [[]] and b will be []
                            # Which fits y = wX + b dimentionality


# Evaluating model performance for a regression using R2 Score
from sklearn.metrics import r2_score
r = r2_score(y_true, y_pred)
print("The R2 score is {:0.3f}".format(r))

# The right way to approach is divide the dataset into 2 parts, training and testing.
from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2)   # 20% for testing, rest for training

# Mean square error can be calculated with
from sklearn.metrics import mean_squared_error as mse

