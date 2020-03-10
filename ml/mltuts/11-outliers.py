import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt

df = pd.read_csv("data/Salary.csv")

# To check distribution (histogram with 20 bins)
df['Salary'].hist(bins=20)
# The distribution of the data doesnt look normal

# Ways to normalize: log, sqrt, cube root

df['Salary_log'] = np.log(df['Salary'])
df['Salary_log'].hist(bins=20)
# The distribution looks fairly normal (gaussian)


df['Salary_sqrt'] = np.sqrt(df['Salary'])
df['Salary_sqrt'].hist(bins=20)
# The distribution looks gaussion with a left bias


df['Salary_cubert'] = np.cbrt(df['Salary'])
df['Salary_cubert'].hist(bins=20)
# The distribution looks gaussion with a left bias


# ------------------------------------------------
# Elliptic envelope: Draws a eclipse and everything outside is outlier

from sklearn.covariance import EllipticEnvelope

X = np.array([
    [100, 100],
    [1, 1],
    [2, 4],
    [4, 5],
    [6, 4],
    [8, 4],
    [6, 2],
    [4, 8],
    [3, 5],
    [7, 2]
])

outlier = EllipticEnvelope(contamination=0.1).fit(X)
prediction1 = outlier.predict(X)
# prediction: array([-1,  1,  1,  1,  1,  1,  1,  1,  1,  1])
# 100, 100 doesn't fit in the eliptical

# Applying it on dataset
# Lets try to find out if age x salary for someone is an outlier
# Means that someone is getting paid a lot MORE for his age
# Doesn't capture outliers which are below a threshold

features = df.iloc[:, [1, 2]].values
outlier = EllipticEnvelope(contamination=0.1).fit(features)
prediction2 = outlier.predict(features)

df['outliers'] = prediction2

# People who are outliers
df[df['outliers'] == -1]
