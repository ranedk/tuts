import statistics as st
import numpy as np

x = range(10)

mean = st.mean(x)

median = st.median(x) # In case of even values, average of the mid-two values 
 
high_median = st.median_high(x) # In case of even, larger of mid-two values

low_median = st.median_low(x) # In case of even, larger of mid-two values

# st.mode  # --  Highest frequency item, if its not unique it throws exception

standard_deviation = st.stdev(x)

variance = st.variance(x)   # measure of variation from mean

# First 1st Quartile
q1 = np.percentile(x, np.arange(0, 100, 25))
# Take x, do a linear interpolation to determine 0th, 25th, 50th, 75th element
# of x and find how many elements are below that element. 

q3 = np.percentile(x, np.arange(0, 100, 75))

# Matrix manipulations

matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
])

np.mean(matrix)         # 5.0  total_all_elements/number_of_elements

np.median(matrix)       # create a list of all numbers, sort, and find median

np.var(matrix)          # create a list of all numbers, and find variance

np.percentile(matrix, 25)  # create a list of all number and then percentile calculation

np.percentile(matrix, 25, axis=0)
# array([2.5, 4. , 4. ])
# 25th percentile across axis 0 (Y)

np.percentile(matrix, 25, axis=1)
# array([1.5, 4.5, 7.5])
# 25th percentile across axis 1 (X)

from scipy import stats

matrix = np.array([
        [1, 2, 1, 3, 4, 6],
        [4, 5, 5, 6, 5, 4],
        [7, 8, 9, 7, 8, 9]
])

stats.mode(matrix, axis=1)
# ModeResult(mode=array([[1], [5], [7]]), count=array([[2], [3], [2]]))
# Along axis=1, find highest frequency number and its count

stats.mode(matrix, axis=None)
#  ModeResult(mode=array([4]), count=array([3]))
# Treat this as a list of number and calculate mode