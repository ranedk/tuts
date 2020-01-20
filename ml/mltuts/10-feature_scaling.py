import numpy as np
from sklearn import preprocessing


# Vector norm:
# The L1 norm that is calculated as the sum of the absolute values of the vector.
# The L2 norm that is calculated as the square root of the sum of the squared vector values.
# The max norm that is calculated as the maximum vector values

x = np.array([
    [-43],
    [-34],
    [0],
    [51],
    [4],
])

# Minmaxscaler: takes a range e.g. 0 to 1 and then maps a given list to the range
# Formula (Xi  - Xmin) / (Xmax - Xmin)

minmaxscaler = preprocessing.MinMaxScaler(feature_range=(0, 1))

print(minmaxscaler.fit_transform(x))

x1 = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
])
print(minmaxscaler.fit_transform(x1))
#[[1. 1. 1.]
# [5. 5. 5.]
# [9. 9. 9.]]
# This takes columns, converts it into a list and then fits in
# Note: For a 3 member list:
    # The first member will always be mapped to the lower limit of the range
    # The last member will always be mapped to the higher limit of the range
    # The middle member will always be mapped to the average of the range
    

# ---------------------------------
# Standard Scaler: Standardizes featires by making mean=0 and scaling to
# unit variance. This makes the data look like a standard normally distributed data
# (i.e. Gaussian with 0 mean and unit variance)

std_scaler = preprocessing.StandardScaler()

print(std_scaler.fit_transform(x))  # Mean of new is  ~ 0

print(std_scaler.fit_transform(x1))

#[[-1.22474487 -1.22474487 -1.22474487]
# [ 0.          0.          0.        ]
# [ 1.22474487  1.22474487  1.22474487]]
# Mean of all columns is now zero

# ---------------------------------
# Normalizer: It normalizes the data in a way that the l1 or the l2 norms are 1

normal = preprocessing.Normalizer()   # by default l2 norm

print(normal.fit_transform(x))

print(normal.fit_transform(x1))
#array([[0.26726124, 0.53452248, 0.80178373],
#       [0.45584231, 0.56980288, 0.68376346],
#       [0.50257071, 0.57436653, 0.64616234]])
# since the normalizer has made the l2 norm of columns equal to 1
sum([i for i in map(lambda x: x*x,  x1norm[0, :])])   # 1.0
sum([i for i in map(lambda x: x*x,  x1norm[1, :])])   # 0.99999
sum([i for i in map(lambda x: x*x,  x1norm[2, :])])   # 1.0


# ---------------------------------
# Binarizer: Normalize into a binary. Everything above a number will be 0, else 1

binarize = preprocessing.Binarizer(threshold=4)
print(binarize.fit_transform(x))
