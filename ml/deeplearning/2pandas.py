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
df.plot(style='.', title='Scatter Plot'); # Plot with dots

# Plot using matplotlib
from matplotlib import pyplot as plt
plt.plot(df)
plt.title('Line plot')
plt.legend(['data1', 'data2', 'data3', 'data4']);

# To see if there is correlation between 2 data points
df.plot(kind='scatter', x='data1', y='data2', xlim=(-1.5, 1.5), ylim=(0, 3), title='Data1 VS Data2');


# Histogram to check frequency of occurence of data. It can be normal, exponential etc
# The data is divided into 50 ranges (bins) and number of data points in that bin are plotted against the range
df.plot(kind='hist', bins=50, title='Histogram', alpha=0.6); # bins to decide the number of buckets


# Cummulative distribution helps understand what fraction of samples are below a bin
df.plot(kind='hist', bins=100, title='Cumulative distributions', density=True, cumulative=True, alpha=0.4);

# Box plots help understand a couple of things:
# Median of the data, Gaussian approximation confidence internval, If data is biased around the median, Outliers in the data
df.plot(kind='box', title='Boxplot');

# Subplots - multiple plots in the same graph

# Plot graph as 2x2 figure
fig, ax = plt.subplots(2, 2, figsize=(16,12))

# plot 1 for 0,0 position
df.plot(ax=ax[0][0], title='Line plot')

# plot 2 for 0,1 position
df.plot(ax=ax[0][1], style='o', title='Scatter plot')

# plot 3 for 1,0 position
df.plot(ax=ax[1][0], kind='hist', bins=50, title='Histogram')

# plot 4 for 1,1 position
df.plot(ax=ax[1][1], kind='box', title='Boxplot');

# Pie charts generally used to project value counts
gt01 = df['data1'] > 0.1    # Label data (True or False) where data1 is greater than 0.1. Get it as dataframe gt01
piecounts = gt01.value_counts()   # Get value counts of True and False
piecounts.plot(kind='pie', figsize=(5, 5), explode=[0, 0.15], labels=['<= 0.1', '> 0.1'], autopct='%1.1f%%', shadow=True, startangle=90, fontsize=16);

# Hexbin plot: Used to draw bins in 2D space

# Create 2 datasets with (x,y) points, distributed around (0,0) and (9,9)
dat1 = np.random.normal((0, 0), 2, size=(1000, 2))
dat2 = np.random.normal((9, 9), 3, size=(2000, 2))
data = np.vstack([dat1, dat2])
df = pd.DataFrame(data, columns=['x', 'y'])  # Vertically stack data1, data2 and label the points 'x' and 'y'

# Draw hexbin which shows in 2D space the distribution and the centers of the distributions
# We can also do a scatter plot, but hexbin creates bins and color codes the density
df.plot(kind='hexbin', x='x', y='y', bins=100, cmap='rainbow', title='Hexbin Plot');
