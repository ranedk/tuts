#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 18:12:55 2019

@author: rane
"""

import pandas as pd

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                    index=[0, 2, 3,4])

df2 = pd.DataFrame({'A1': ['A4', 'A5', 'A6', 'A7'],
                    'C': ['C4', 'C5', 'C6', 'C7'],
                    'D2': ['D4', 'D5', 'D6', 'D7']},
                    index=[ 4, 5, 6 ,7])

print(df1)
print(df2)

pd.concat([df1, df2], axis=1, ignore_index=True)
# pd.concat([df1, df2], axis=1)  # ignore_index is redundant here, same result

#     0    1    2    3    4    5
#0   A0   B0   D0  NaN  NaN  NaN
#2   A1   B1   D1  NaN  NaN  NaN
#3   A2   B2   D2  NaN  NaN  NaN
#4   A3   B3   D3   A4   C4   D4  <-- concat because axis=1
#5  NaN  NaN  NaN   A5   C5   D5
#6  NaN  NaN  NaN   A6   C6   D6
#7  NaN  NaN  NaN   A7   C7   D7

pd.concat([df1, df2])

#     A   A1    B    C    D   D2
#0   A0  NaN   B0  NaN   D0  NaN
#2   A1  NaN   B1  NaN   D1  NaN
#3   A2  NaN   B2  NaN   D2  NaN
#4   A3  NaN   B3  NaN   D3  NaN <-- no concat, axis not specified
#4  NaN   A4  NaN   C4  NaN   D4 <-- no concat
#5  NaN   A5  NaN   C5  NaN   D5
#6  NaN   A6  NaN   C6  NaN   D6
#7  NaN   A7  NaN   C7  NaN   D7

pd.concat([df1, df2], ignore_index=True)

#     A   A1    B    C    D   D2
#0   A0  NaN   B0  NaN   D0  NaN
#1   A1  NaN   B1  NaN   D1  NaN
#2   A2  NaN   B2  NaN   D2  NaN
#3   A3  NaN   B3  NaN   D3  NaN <-- no concat and re-indexed
#4  NaN   A4  NaN   C4  NaN   D4
#5  NaN   A5  NaN   C5  NaN   D5
#6  NaN   A6  NaN   C6  NaN   D6
#7  NaN   A7  NaN   C7  NaN   D7

df1.reset_index(drop=True, inplace=True)  # redo indexes
df2.reset_index(drop=True, inplace=True)  # redo indexes

print(df1)
print(df2)

pd.concat([df1, df2], axis=1)

#    A   B   D  A1   C  D2
#0  A0  B0  D0  A4  C4  D4
#1  A1  B1  D1  A5  C5  D5
#2  A2  B2  D2  A6  C6  D6
#3  A3  B3  D3  A7  C7  D7
