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

x = np.array([
    []
])

outlier = EllipticEnvelope(contamination=0.1)
outlier.fix(df['Salary'])