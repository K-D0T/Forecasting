import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib
from pylab import rcParams

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
SIN = ['GAVOUC0524CHICK']
df = pd.read_excel("Simmons_forcasting.xls")
GAVOUC0524CHICK = df.loc[df['2ndItemNumber'] == 'GAVOUC0524CHICK']
print(GAVOUC0524CHICK)
y = GAVOUC0524CHICK['Date'].min(), GAVOUC0524CHICK['Date'].max()



GAVOUC0524CHICK = GAVOUC0524CHICK.groupby('Date')['Volume'].sum().reset_index()
print(GAVOUC0524CHICK)
GAVOUC0524CHICK = GAVOUC0524CHICK.set_index('Date')
GAVOUC0524CHICK.index = pd.to_datetime(GAVOUC0524CHICK.index)
k = GAVOUC0524CHICK.index
print(k)
GAVOUC0524CHICK.plot(figsize=(15, 6))
#plt.show()



y = GAVOUC0524CHICK['Volume'].resample('MS').mean()
y['2019':]
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

for param in pdq:
	for param_seasonal in seasonal_pdq:
		try:
			mod = sm.tsa.statespace.SARIMAX(y, order=param, seasonal_order=param_seasonal, enforce_stationarity=False, enforce_invertibility=False)
			results = mod.fit()
			print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
		except:

			continue 
mod = sm.tsa.statespace.SARIMAX(y, order=(1, 1, 1), seasonal_order=(1, 1, 0, 12), enforce_stationarity=False, enforce_invertibility=False)

results = mod.fit()
print(results.summary().tables[1])
#results.plot_diagnostics(figsize=(16, 8))
#plt.show()

pred = results.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()
#ax = y['2010':].plot(label='observed')
#pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
#ax.fill_between(pred_ci.index,
                #pred_ci.iloc[:, 0],
                #pred_ci.iloc[:, 1], color='k', alpha=.2)
#ax.set_xlabel('Date')
#ax.set_ylabel('GAVOUC0524CHICK Volume')
#plt.legend()
#plt.show()
y_forecasted = pred.predicted_mean
y_truth = y['2017-01-01':]
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

pred_uc = results.get_forecast(steps=10)
pred_ci = pred_uc.conf_int()
def Average(pred_ci):
	return sum(pred_ci) / len(pred_ci)

print(SIN, pred_ci)
#ax = y.plot(label='observed', figsize=(14, 7))
#pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
#ax.fill_between(pred_ci.index,
                #pred_ci.iloc[:, 0],
                #pred_ci.iloc[:, 1], color='k', alpha=.25)
#ax.set_xlabel('Date')
#ax.set_ylabel('Volume')
#plt.legend()
#plt.show()