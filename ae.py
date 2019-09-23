import numpy as np
import csv
import pandas as pd
import json
from itertools import zip_longest

def ApEn(U, m, r):

    def _maxdist(x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(m):
        x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0) for x_i in x]
        return (N - m + 1.0)**(-1) * sum(np.log(C))

    N = len(U)

    return abs(_phi(m+1) - _phi(m))


with open('gcode123.json') as f:
    columns = json.load(f)


df = pd.read_csv('ktml32.csv', skipinitialspace=True, usecols=columns)


l = []
p = []
bad_gcodes = []
bad_num = []
print("Checking Forecastability Matrix...")
for ae in columns:
    l.append(ae)
    k = df[ae]

    p.append(ApEn(k, 2, 3))
    apen = (ApEn(k, 2, 3))

    #print(apen)
    if apen > 0.5:
        bad_gcodes.append(ae)
        bad_num.append(apen)
        print("Yeah")

print(bad_gcodes)

#print(gcode)

df = pd.DataFrame(list(zip(*[bad_gcodes, bad_num])))

df.to_csv('Forcastablity_Bad.csv', index=False)

#print(df)

df = pd.DataFrame(list(zip(*[l, p])))

df.to_csv('Forcastablity_Good.csv', index=False)

#print(df)

