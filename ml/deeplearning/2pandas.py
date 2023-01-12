import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


N = 1000
# generate N points gaussian distributed with std-deviation of 0.1
data1 = np.random.normal(0, 0.1, N)

# generate gaussian distributed and push all points linearly increasing from 0 to 1 
data2 = (np.random.normal(1, 0.4, N) + np.linspace(0, 1, N))

# generate uniformally distributed data, with uniformally increased by 2 and linearly increasing from 1 to 5
data3 = 2 + (np.random.random(N) + np.linspace(1, 5, N))

# 2 + generate uniformally distributed data scaling it with data points linearly increasing from 1 to 5
data4 = 2 + (np.random.random(N) * np.linspace(1, 5, N))

# gaussian distributed data increased with a sine data
data5 = (np.random.normal(3, 0.2, N) + 0.3 * np.sin(np.linspace(0, 20, N)))


# Create a data frame with data vertically stacked
data = np.vstack([data1, data2, data3, data4, data5])
data = data.transpose()
cols = ['data1', 'data2', 'data3', 'data4', 'data5']
df = pd.DataFrame(data, columns=cols)

# Plotting using dataframe:
df.plot(title='Line plot');

# Plot using matplotlib
from matplotlib import pyplot as plt
plt.plot(df)
plt.title('Line plot')
plt.legend(['data1', 'data2', 'data3', 'data4']);


